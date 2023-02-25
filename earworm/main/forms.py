from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError, InputRequired
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea

from earworm.models import Artist, Album, Review, Genre

class ArtistMixin(FlaskForm):
    """Form for adding/updating an Artist."""
    name = StringField('Name', validators=[DataRequired()])
    bio = StringField('Biography', widget=TextArea(), validators=[Length(max=9000)])
    photo_url = StringField('Photo URL', validators=[URL()])

    def validate_bio(self, bio):
        """Validate that the artist bio is at least 10 characters."""
        if len(bio.data) < 10:
            raise ValidationError('Your bio must be at least 10 characters.')
        if len(bio.data) > 9000:
            raise ValidationError('Your bio must be less than 9000 characters.')

class ArtistForm(ArtistMixin):
    submit = SubmitField('Add Artist')
    def validate_name(self, name):
        """Validate that the artist name is unique."""
        artist = Artist.query.filter_by(name=name.data).first()
        if artist:
            raise ValidationError('Artist already exists. Please choose a different artist name.')
      
class ArtistUpdateForm(ArtistMixin):
    submit = SubmitField('Update Artist')

class AlbumMixin(FlaskForm):
    """Form basis for Albums."""
    title = StringField('Album Title', validators=[DataRequired()])
    artist = QuerySelectField(query_factory=lambda: Artist.query, get_label='name')
    release_date = DateField('Release Date', validators=[DataRequired()], format='%Y-%m-%d')
    cover_url = StringField('Cover URL', validators=[URL()])
    genre = SelectField('Genre', choices=Genre.choices())


class AlbumForm(AlbumMixin):
    """Form for adding an Album. Inherits from AlbumMixin."""
    submit = SubmitField('Add Album')

    def validate_title(self, title):
        """Validate that the album title is unique for the artist."""
        artist_id = self.artist.data.id
        album = Album.query.filter(Album.title == title.data, Album.artist == artist_id).first()
        if album:
            raise ValidationError('Album already exists for this artist. Maybe you want to edit it?')

class AlbumUpdateForm(AlbumMixin):
    """Form for updating an Album. Inherits from AlbumMixin."""
    submit = SubmitField('Update Album')

class AlbumFromArtistForm(AlbumMixin):
    submit = SubmitField('Add Album')


class ReviewFormMixin(FlaskForm):
    """Form for adding/updating a Review. Inherits from AlbumMixin."""
    album = QuerySelectField(query_factory=lambda: Album.query, get_label='title', allow_blank=False, blank_text='Select Album')
    rating = HiddenField('Rating', validators=[InputRequired()])
    summary = StringField('One line summary', validators=[DataRequired(), Length(max=255)])
    content = StringField('Full review', widget=TextArea(), validators=[DataRequired(), Length(min=80)])

    def validate_summary(self, summary):
        """Validate that the summary is at most 255 characters."""
        if len(summary.data) > 255:
            raise ValidationError('Your summary must be less than 255 characters.')

    def validate_content(self, content):
        """ Validate that the review is at least 10 characters."""
        if len(content.data) < 10:
            raise ValidationError('Your review must be at least 10 characters.')

class ReviewForm(ReviewFormMixin):
    """Form for adding a Review. Inherits from ReviewFormMixin."""
    submit = SubmitField('Add Review')

    def validate_user_review(self, album):
        """Validate that the user has not already reviewed the album."""
        user_id = current_user.id
        album_id = album.data.id
        review = Review.query.filter(Review.user_id == user_id, Review.album_id == album_id).first()
        if review:
            raise ValidationError('You have already reviewed this album. You can edit your review below.')

class ReviewUpdateForm(ReviewFormMixin):
    """Form for updating a Review. Inherits from ReviewFormMixin."""
    submit = SubmitField('Update Review')

