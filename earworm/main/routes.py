from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from flask_login import login_required, current_user
from earworm.extensions import app, db

from earworm.models import Artist, Album, Review
from earworm.main.forms import ArtistForm, ArtistUpdateForm, AlbumForm, ReviewForm

##########################################
#           Routes                       #
##########################################

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('Admin/home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.args.get('query')
    print(search_term)
    return redirect(url_for('main.search_results', search_term=search_term))

@main.route('/search_results/<search_term>', methods=['GET', 'POST'])
def search_results(search_term):
    search_term = search_term
    artist_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    album_results = Album.query.filter(Album.title.ilike(f'%{search_term}%')).all()
    review_results = Review.query.filter(Review.content.ilike(f'%{search_term}%')).all()
    return render_template('Admin/search_results.html', artist_results=artist_results, album_results=album_results, review_results=review_results, search_term=search_term)

@main.route('/about')
def about():
    return render_template('Admin/about.html')

@main.route('/contact')
def contact():
    return render_template('Admin/contact.html')

@main.route('/all_earworms', methods=['GET', 'POST'])
def all_earworms():
    all_reviews = Review.query.order_by(Review.date_created.desc()).all()
    all_artists = Artist.query.order_by(Artist.name).all()
    all_albums = Album.query.order_by(Album.title).all()
    return render_template('Admin/all_earworms.html', reviews=all_reviews, artists=all_artists, albums=all_albums)

@main.route('/add_artist', methods=['GET', 'POST'])
@login_required
def add_artist():
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
@login_required
def artist_detail(artist_id):
    artist = Artist.query.get(artist_id)
    albums = Album.query.filter_by(artist=artist_id).all()
    return render_template('Artists/artist_detail.html', artist=artist, albums=albums)

@main.route('/edit/<artist_id>', methods=['GET','POST'])
@login_required
def edit_artist(artist_id):
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
    form = AlbumForm()
    if form.validate_on_submit():
        new_album = Album(
            title=form.title.data,
            release_date=form.release_date.data,
            artist=form.artist.data.id,
            cover_url=form.cover_url.data,
            genre=form.genre.data
        )
        db.session.add(new_album)
        db.session.commit()
        flash('Album added successfully!')
        return redirect(url_for('main.album_detail', album_id=new_album.id))
    return render_template('Albums/add_album.html', form=form)

@main.route('/album/<album_id>', methods=['GET', 'POST'])
def album_detail(album_id):
    album = Album.query.get(album_id)
    artist = Artist.query.get(album.artist)
    return render_template('Albums/album_detail.html', album=album, artist=artist)

@main.route('/album/<album_id>/edit', methods=['POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get(album_id)
    form = AlbumForm(obj=album)

    if form.validate_on_submit():
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.artist_id = form.artist_id.data
        album.cover_url = form.cover_url.data
        album.genre = form.genre.data
        db.session.commit()
        flash('Album updated successfully!')
        return redirect(url_for('main.album_detail', album_id=album.id))
    return render_template('Albums/album_edit.html', album=album, form=form)

@main.route('/create_review', methods=['GET', 'POST'])
@login_required
def create_review():
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(
            summary=form.summary.data,
            content=form.content.data,
            rating=form.rating.data,
            reviewed_album=form.album.data.id,
            date_created=datetime.now()
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!')
        return redirect(url_for('main.review_detail', review_id=new_review.id))
    return render_template('Reviews/create_review.html', form=form)

@main.route('/review/<review_id>', methods=['GET', 'POST'])
def review_detail(review_id):
    review = Review.query.get(review_id)
    form = ReviewForm(obj=review)

    if form.validate_on_submit():
        review.title = form.title.data
        review.content = form.content.data
        review.rating = form.rating.data
        review.album_id = form.album_id.data
        review.date_updated = datetime.now()
        db.session.commit()
        flash('Review updated successfully!')
        return redirect(url_for('main.review_detail', review_id=review.id))
    return render_template('Reviews/review_detail.html', review=review, form=form)
