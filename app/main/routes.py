from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from flask_login import login_required
from app.extensions import app, db

from app.models import Artist, Album, Review
from app.main.forms import ArtistForm, AlbumForm, ReviewForm

##########################################
#           Routes                       #
##########################################

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        return redirect(url_for('main.search_results', search_term=search_term))
    return render_template('search.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/all_earworms', methods=['GET', 'POST'])
def all_earworms():
    all_reviews = Review.query.all()
    all_artists = Artist.query.all()
    all_albums = Album.query.all()
    return render_template('all_earworms.html', reviews=all_reviews, artists=all_artists, albums=all_albums)

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
    return render_template('add_artist.html', form=form)

@main.route('/artist/<artist_id>', methods=['GET', 'POST'])
@login_required
def artist_detail(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    if form.validate_on_submit():
        artist.name = form.name.data
        artist.photo_url = form.photo_url.data
        db.session.commit()
        
        flash('Artist updated successfully!')
        return redirect(url_for('main.artist_detail', artist_id=artist.id))
    return render_template('artist_detail.html', artist=artist, form=form)

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
    return render_template('add_album.html', form=form)

@main.route('/album/<album_id>', methods=['GET', 'POST'])
@login_required
def album_detail(album_id):
    album = Album.query.get(album_id)
    artist = Artist.query.get(album.artist)
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
    return render_template('album_detail.html', album=album, form=form, artist=artist)

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
    return render_template('create_review.html', form=form)

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
    return render_template('review_detail.html', review=review, form=form)
