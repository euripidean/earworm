import app
from unittest import TestCase
from earworm.models import User
from earworm.extensions import app, db, bcrypt

#################################################
# Setup
#################################################
def create_user():
    password_hash = bcrypt.generate_password_hash('password1234!').decode('utf-8')
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
            'password': 'password1234!',
        }

        self.app.post('/signup', data=post_data, follow_redirects=True)
        user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(user)

    def test_signup_existing_user(self):
        """Test that a user cannot sign up with an existing username"""
        create_user()
        post_data = {
            'username': 'test_user',
            'password': 'password1234!',
        }
        new_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(new_user)
        response = self.app.post('/signup', data=post_data, follow_redirects=True)
        self.assertIn(b'Username already exists. Please choose a different one.', response.data)

    def test_login_incorrect_password(self):
        """Test that a user cannot login with an incorrect password"""
        create_user()
        response = login(self.app, 'test_user', 'incorrect_password')
        self.assertIn(b'Username or password does not match. Please try again.', response.data)

    def test_login_correct_password(self):
        """Test that a user can login with the correct password"""
        create_user()
        response = login(self.app, 'test_user', 'password1234!')
        self.assertIn(b'You are now logged in.', response.data)

    def test_login_nonexistent_user(self):
        """Test that a user cannot login with a nonexistent username"""
        post_data = {
            'username': 'not_a_user',
            'password': 'password1234!',
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        self.assertIn(b'There is no account with that username. Please try again.', response.data)

    def test_logout(self):
        """Test that a user can logout"""
        create_user()
        post_data = {
            'username': 'test_user',
            'password': 'password1234!',
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        self.assertIn(b'You are now logged in.', response.data)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Logged out successfully.', response.data)

