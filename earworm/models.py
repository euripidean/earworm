from sqlalchemy_utils import URLType
from flask_login import UserMixin

from earworm.extensions import db
from earworm.utils import FormEnum


class Genre(FormEnum):
    """Genre enum."""
    POP = 'Pop'
    ROCK = 'Rock'
    COUNTRY = 'Country'
    HIP_HOP = 'Hip-Hop'
    RAP = 'Rap'
    R_AND_B = 'R&B'
    JAZZ = 'Jazz'
    BLUES = 'Blues'
    CLASSICAL = 'Classical'
    METAL = 'Metal'
    ELECTRONIC = 'Electronic'
    FOLK = 'Folk'
    REGGAE = 'Reggae'
    SOUL = 'Soul'
    PUNK = 'Punk'
    INDIE = 'Indie'
    OTHER = 'Other'

class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    public = db.Column(db.Boolean, nullable=False, default=True)
    liked_artists = db.relationship('Artist', secondary="artist_listeners", backref='user', lazy=True, cascade="all, delete")
    reviews_written = db.relationship('Review', backref='user', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'User({self.username})'
    
    def __str__(self):
        return self.username


class Artist(db.Model):
    """Artist model."""
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(9000), nullable=True)
    photo_url = db.Column(URLType, nullable=True)
    listeners = db.relationship('User', secondary="artist_listeners" , backref='artist', lazy=True, cascade="all, delete")


    def __repr__(self):
        return f'Artist({self.name})'
    
    def __str__(self):
        return self.name

class Album(db.Model):
    """Album model."""
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    cover_url = db.Column(URLType, nullable=True)
    genre = db.Column(db.Enum(Genre), nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    date_added = db.Column(db.Date, nullable=False)
    reviews = db.relationship('Review', backref='album', lazy=True, cascade="all, delete")
    
   
    def __repr__(self):
        return f'Album({self.title})'
    
    def __str__(self):
        return self.title

class Review(db.Model):
    """Review model."""
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    date_updated = db.Column(db.Date, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewed_album = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    written_by = db.relationship('User', backref='review', lazy=True, cascade="all, delete")
    albums = db.relationship('Album', backref='review', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'Review({self.summary})'
    
    def __str__(self):
        return self.summary

user_artist_table = db.Table('artist_listeners',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)

user_review_table = db.Table('user_reviews',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True)
)

album_review_table = db.Table('album_reviews',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True)
)
