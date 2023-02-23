from sqlalchemy_utils import URLType
from flask_login import UserMixin

from earworm.extensions import app, db
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
    username = db.Column(db.Text(50), nullable=False)
    password = db.Column(db.Text(50), nullable=False)
    avatar_url = db.Column(URLType, nullable=True)
    public = db.Column(db.Boolean, nullable=False, default=True)
    liked_artists = db.relationship('Artist', secondary="artist_listeners", backref='user', lazy=True)

class Artist(db.Model):
    """Artist model."""
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50), nullable=False)
    bio = db.Column(db.Text(500), nullable=True)
    photo_url = db.Column(URLType, nullable=True)
    listeners = db.relationship('User', secondary="artist_listeners" , backref='artist', lazy=True)

    def __repr__(self):
        return f'Artist({self.name})'

class Album(db.Model):
    """Album model."""
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    cover_url = db.Column(URLType, nullable=True)
    genre = db.Column(db.Enum(Genre), nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    def __repr__(self):
        return f'Album({self.title})'

class Review(db.Model):
    """Review model."""
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_url = db.Column(URLType, nullable=True)
    date_created = db.Column(db.Date, nullable=False)
    date_updated = db.Column(db.Date, nullable=True)
    reviewed_album = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    def __repr__(self):
        return f'Review({self.rating}, {self.content})'

user_artist_table = db.Table('artist_listeners',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)
