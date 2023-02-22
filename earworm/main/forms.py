from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea

from earworm.models import Artist, Album, Review, Genre

class ArtistForm(FlaskForm):
    # TODO: Look into using mixins to change submit button text based on whether the form is for adding or updating.
    """Form for adding/updating an Artist."""
    name = StringField('Name', validators=[DataRequired()])
    bio = StringField('Biography', widget=TextArea(), validators=[Length(max=500)])
    photo_url = StringField('Photo URL', validators=[URL()])
    submit = SubmitField('Add Artist')
    
    def validate_name(self, name):
        """Validate that the artist name is unique."""
        artist = Artist.query.filter_by(name=name.data).first()
        if artist:
            raise ValidationError('Artist already exists. Please choose a different artist name.')

    def validate_bio(self, bio):
        """Validate that the artist bio is at least 10 characters."""
        if len(bio.data) < 10:
            raise ValidationError('Your bio must be at least 10 characters.')
        if len(bio.data) > 500:
            raise ValidationError('Your bio must be less than 500 characters.')

class AlbumForm(FlaskForm):
    """Form for adding/updating an Album."""
    title = StringField('Album Title', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()], format='%Y-%m-%d')
    artist = QuerySelectField(query_factory=lambda: Artist.query, get_label='name')
    cover_url = StringField('Cover URL', validators=[URL()])
    genre = SelectField('Genre', choices=Genre.choices())
    submit = SubmitField('Add Album')

    # TODO: Add validation to ensure that the album title is unique for the artist.
    # def validate_title(self, title):
    #     """Validate that the album title is unique for the artist."""
    #     album = Album.query.filter_by(title=title.data).first()
    #     if album:
    #         raise ValidationError('Album already exists for this artist. Please choose a different album title.')


class ReviewForm(FlaskForm):
    """Form for adding/updating a Review. STRETCH GOALS: Make rating field selectable stars 
    and pull through artist name dynamically based on album selection."""
    album = QuerySelectField(query_factory=lambda: Album.query, get_label='title')
    summary = StringField('Summary', validators=[DataRequired(), Length(max=255)])
    rating = SelectField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    content = StringField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Add Review')

    def validate_summary(self, summary):
        """Validate that the summary is at most 255 characters."""
        if len(summary.data) > 255:
            raise ValidationError('Your summary must be less than 255 characters.')

    def validate_content(self, content):
        """ Validate that the review is at least 10 characters."""
        if len(content.data) < 10:
            raise ValidationError('Your review must be at least 10 characters.')

    def validate_album_id(self, album):
        """Validate that the user has not already reviewed this album."""
        review = Review.query.filter_by(album_id=album.data.id).filter_by(user_id=current_user.id).first()
        if review:
            raise ValidationError('You have already reviewed this album.')

# class SearchForm(FlaskForm):
#     """Form for searching for an album, artist or other user."""
#     search = StringField('Search', validators=[DataRequired()])
#     submit = SubmitField('Search')

    def validate_search(self, search):
        """Validate that the search term is at least 3 characters."""
        if len(search.data) < 3:
            raise ValidationError('Search term must be at least 3 characters.')

