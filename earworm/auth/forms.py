from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, url, ValidationError, optional
from earworm.extensions import app, db, bcrypt

from earworm.models import User

class SignUpFormMixin(FlaskForm):
    """Sign up form."""
    password = PasswordField('Password', validators=[InputRequired()])
    avatar_url = StringField('Avatar URL', validators=[optional(), url()])
    bio = StringField('Bio', validators=[optional(), Length(max=255)])
    public = BooleanField('Would you like your profile to be public?')
    

        
class SignUpForm(SignUpFormMixin):
    """Sign up form."""
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validate username."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
        
class UserUpdateForm(SignUpFormMixin):
    """User update form."""
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10, max=50)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        """Validate username."""
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('There is no account with that username. Please try again.')

    def validate_password(self, password):
        """Validate password."""
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Password does not match. Please try again.')
