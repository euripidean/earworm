import app
from unittest import TestCase
from earworm.models import User, Artist, Album, Review
from earworm.extensions import app, db, bcrypt

#################################################
# Setup
#################################################

def create_user():
    password_hash = bcrypt.generate_password_hash('password1234!').decode('utf-8')
    username = 'test_user'
    bio = 'I was born in a small town in the middle of nowhere.'
    avatar_url = 'http://t0.gstatic.com/licensed-image?q=tbn:ANd9GcS8DxAOFrR9zmRLqyH6eGk-XEIfkcvafCKPNqR1YduokqF6tlCkZQEQ_EVJypF9uyekuU9S2aeC9wayhog'
    user = User(username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()
