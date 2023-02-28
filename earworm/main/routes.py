from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from flask_login import login_required, current_user
from earworm.extensions import app, db

from earworm.models import Artist, Album, Review, User
from earworm.main.forms import ArtistForm, ArtistUpdateForm, AlbumForm, AlbumUpdateForm, ReviewUpdateForm, ReviewForm


##########################################
#           Routes                       #
##########################################

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    """Renders splash page for log in or sign up."""
    if current_user.is_authenticated:
        return redirect(url_for('main.all_earworms'))
    return render_template('Admin/home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    """Searches for a term in the database."""
    search_term = request.args.get('query')
    if not search_term:
        return redirect(url_for('main.all_earworms'))
    return redirect(url_for('main.search_results', search_term=search_term))

@main.route('/search_results/<search_term>', methods=['GET', 'POST'])
def search_results(search_term):
    """Renders search results page."""
    search_term = search_term
    albums = Album.query.all()
    artists = Artist.query.all()
    artist_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    album_results = Album.query.filter(Album.title.ilike(f'%{search_term}%')).all()
    review_results = Review.query.filter(Review.content.ilike(f'%{search_term}%')).all()
    user_results = User.query.filter(User.username.ilike(f'%{search_term}%')).all()
    return render_template(
        'Admin/search_results.html', 
        artist_results=artist_results, 
        album_results=album_results, 
        review_results=review_results, 
        user_results=user_results, 
        search_term=search_term, 
        artists=artists,
        albums=albums)

@main.route('/about')
def about():
    """Renders about page."""
    return render_template('Admin/about.html')

@main.route('/contact')
def contact():
    """Renders contact page."""
    return render_template('Admin/contact.html')

@main.route('/all_earworms', methods=['GET', 'POST'])
def all_earworms():
    """Renders all earworms page. Information is limited to prevent clutter."""
    all_reviews = Review.query.order_by(Review.date_created.desc()).all()
    all_artists = Artist.query.order_by(Artist.name).all()
    all_albums = Album.query.order_by(Album.title).all()
    public_users = User.query.filter_by(public=True).all()
    return render_template('Admin/all_earworms.html', reviews=all_reviews, artists=all_artists, users=public_users, albums=all_albums)

@main.route('/add_artist', methods=['GET', 'POST'])
@login_required
def add_artist():
    """Renders add artist page and adds artist to database."""
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data,
            photo_url=form.photo_url.data,
            bio=form.bio.data
        )
        db.session.add(new_artist)
        db.session.commit()

        flash('Artist added successfully!')
        return redirect(url_for('main.artist_detail', artist_id=new_artist.id))
    return render_template('Artists/add_artist.html', form=form)

@main.route('/artist/<artist_id>', methods=['GET', 'POST'])
def artist_detail(artist_id):
    """Renders artist detail page."""
    artist = Artist.query.get(artist_id)
    albums = Album.query.filter_by(artist=artist.id).order_by(Album.release_date.desc()).all()
    listener_count = len(artist.listeners)
    listeners = [user for user in artist.listeners]
    return render_template('Artists/artist_detail.html', artist=artist, albums=albums, listener_count=listener_count, users=listeners)

@main.route('/all_artists', methods=['GET', 'POST'])
def all_artists():
    """Renders all artists page with artists listed in alphabetical order."""
    all_artists = Artist.query.order_by(Artist.name).all()
    return render_template('Artists/all_artists.html', artists=all_artists)

@main.route('/edit/artist/<artist_id>', methods=['GET','POST'])
@login_required
def edit_artist(artist_id):
    """Renders edit artist page and updates artist in database."""
    artist = Artist.query.get(artist_id)
    form = ArtistUpdateForm(obj=artist)
    if form.validate_on_submit():
        artist.name = form.name.data
        artist.photo_url = form.photo_url.data
        artist.bio = form.bio.data
        db.session.commit()
        flash('Artist updated successfully!')
        return redirect(url_for('main.artist_detail', artist_id=artist.id))
    artist = Artist.query.get(artist_id)
    return render_template('Artists/artist_edit.html', artist=artist, form=form)

@main.route('/add_album', methods=['GET', 'POST'])
@login_required
def add_album():
    """Renders add album page and adds album to database."""
    artist = request.args.get('artist_id')
    artist = Artist.query.get(artist)
    form = AlbumForm()
    if artist:
        form.artist.data = artist
    if form.validate_on_submit():
        new_album = Album(
            title=form.title.data,
            release_date=form.release_date.data,
            artist=form.artist.data.id,
            cover_url=form.cover_url.data,
            genre=form.genre.data,
            date_added=datetime.now()
        )
        db.session.add(new_album)
        db.session.commit()
        flash('Album added successfully!')
        return redirect(url_for('main.album_detail', album_id=new_album.id))
    return render_template('Albums/add_album.html', form=form)

@main.route('/all_albums', methods=['GET', 'POST'])
def all_albums():
    """Renders all albums page with albums listed in alphabetical order."""
    all_albums = Album.query.order_by(Album.title).all()
    artist = [Artist.query.get(album.artist) for album in all_albums]
    return render_template('Albums/all_albums.html', albums=all_albums, artist=artist)

@main.route('/album/<album_id>', methods=['GET', 'POST'])
def album_detail(album_id):
    """Renders album detail page. If current user has reviewed album, 
    removes add review button and replaces it with edit review."""
    album = Album.query.get(album_id)
    artist = Artist.query.get(album.artist)
    reviews = Review.query.filter_by(reviewed_album=album.id).order_by(Review.date_created.desc()).all()
    # if any review is by current user return true
    review = None
    review_exists = False
    if reviews:
        review_exists = any(review.created_by == current_user.id for review in reviews)
    if review_exists:
        review = Review.query.filter_by(created_by=current_user.id, reviewed_album=album.id).first()
    return render_template('Albums/album_detail.html', album=album, artist=artist, reviews=reviews, review_exists=review_exists, review=review)

@main.route('/edit/album/<album_id>', methods=['GET','POST'])
@login_required
def edit_album(album_id):
    """Renders edit album page and updates album in database."""
    album = Album.query.get(album_id)
    genre = album.genre
    artist = Artist.query.get(album.artist)
    form = AlbumUpdateForm(obj=album)
    form.artist.data = artist
    form.genre.data = genre.name

    if form.validate_on_submit():
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.artist = form.artist.data.id
        album.cover_url = form.cover_url.data
        album.genre = form.genre.data
        db.session.commit()
        flash('Album updated successfully!')
        return redirect(url_for('main.album_detail', album_id=album.id))
    album = Album.query.get(album_id)
    return render_template('Albums/album_edit.html', album=album, form=form)

@main.route('/create_review', methods=['GET', 'POST'])
@login_required
def create_review():
    """Renders create review page and adds review to database."""
    album = request.args.get('album_id')
    album = Album.query.get(album)
    rating = request.form.get('rating')
 
    form = ReviewForm()
    if album:
        form.album.data = album
    if form.validate_on_submit():
        new_review = Review(
            summary=form.summary.data,
            content=form.content.data,
            rating= rating,
            reviewed_album= form.album.data.id,
            date_created=datetime.now(),
            created_by=current_user.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!')
        return redirect(url_for('main.review_detail', review_id=new_review.id))
    return render_template('Reviews/create_review.html', form=form)

@main.route('/review/<review_id>', methods=['GET', 'POST'])
def review_detail(review_id):
    """Renders review detail page. If current user is the author of the review,
    shows edit review and delete button."""
    review = Review.query.get(review_id)
    form = ReviewForm(obj=review)
    album = Album.query.get(review.reviewed_album)
    artist = Artist.query.get(album.artist)
    user = User.query.get(review.created_by)
    return render_template('Reviews/review_detail.html', review=review, form=form, album=album, artist=artist, user=user)

@main.route('/edit/review/<review_id>', methods=['GET','POST'])
@login_required
def edit_review(review_id):
    """Renders edit review page and updates review in database."""
    rating = request.form.get('rating')
    review = Review.query.get(review_id)
    album = Album.query.get(review.reviewed_album)
    form = ReviewUpdateForm(obj=review)
    form.album.data = album

    if form.validate_on_submit():
        review.summary = form.summary.data
        review.content = form.content.data
        review.rating = rating
        review.reviewed_album = form.album.data.id
        review.date_updated = datetime.now()
        db.session.commit()
        flash('Review updated successfully!')
        return redirect(url_for('main.review_detail', review_id=review.id))
    review = Review.query.get(review_id)
    return render_template('Reviews/review_edit.html', review=review, form=form, edit=True)

@main.route('/delete/review/<review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    """Deletes review from database."""
    review = Review.query.get(review_id)
    artist = Artist.query.get(review.reviewed_album)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully!')
    return redirect(url_for('main.artist_detail', artist_id=artist.id))

@main.route('/follow/<artist_id>', methods=['GET', 'POST'])
@login_required
def like_artist(artist_id):
    """Adds artist to current user's liked artists list."""
    artist = Artist.query.get(artist_id)
    if artist not in current_user.liked_artists:
        current_user.liked_artists.append(artist)
        db.session.commit()
        flash('Artist followed!')
    else:
        flash('You already follow this artist!')
    return redirect(url_for('main.artist_detail', artist_id=artist.id))

@main.route('/unfollow/<artist_id>', methods=['GET', 'POST'])
@login_required
def unlike_artist(artist_id):
    """Removes artist from current user's liked artists list."""
    artist = Artist.query.get(artist_id)
    if artist in current_user.liked_artists:
        current_user.liked_artists.remove(artist)
        db.session.commit()
        flash('Artist unfollowed!')
    else:
        flash("You don't follow this artist!")
    return redirect(url_for('main.artist_detail', artist_id=artist.id))
