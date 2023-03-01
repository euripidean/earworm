import os
from unittest import TestCase
from earworm.models import User, Review, Artist
from earworm.extensions import app, db, bcrypt

#################################################
# Setup
#################################################
def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    username = 'test_user'
    user = User(username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)



#################################################
# Tests
#################################################
class AuthTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        """Test for the signup route"""
        post_data = {
            'username': 'test_user',
            'password': 'password',
        }

        self.app.post('/signup', data=post_data, follow_redirects=True)
        user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(user)


       