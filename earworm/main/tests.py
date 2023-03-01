import app
from unittest import TestCase
from datetime import datetime
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
    public = True
    user = User(username=username, password=password_hash, bio=bio, avatar_url=avatar_url, public=public)
    db.session.add(user)
    db.session.commit()

def create_second_user():
    password_hash = bcrypt.generate_password_hash('password1234!').decode('utf-8')
    username = 'test_user2'
    bio = 'I was born in a crossfire hurricane.'
    avatar_url = 'https://upload.wikimedia.org/wikipedia/commons/8/80/Kevin_Hart_2014_%28cropped_2%29.jpg'
    public = False
    user = User(username=username, password=password_hash, bio=bio, avatar_url=avatar_url, public=public)
    db.session.add(user)
    db.session.commit()

def create_artist():
    name = 'The Beatles'
    bio = 'The Beatles were an English rock band formed in Liverpool in 1960. With members John Lennon, Paul McCartney, George Harrison and Ringo Starr, they became widely regarded as the foremost and most influential act of the rock era.'
    photo_url = 'https://upload.wikimedia.org/wikipedia/commons/4/4f/Beatles_-_Ed_Sullivan_Theater_-_New_York_-_February_9%2C_1964.jpg'
    artist = Artist(name=name, bio=bio, photo_url=photo_url)
    db.session.add(artist)
    db.session.commit()

def create_album():
    title = 'Abbey Road'
    artist = 1
    release_date = datetime(1969, 9, 26)
    cover_url = 'https://upload.wikimedia.org/wikipedia/en/9/9f/Abbey_Road_%281969%29.png'
    genre = 'ROCK'
    date_added = datetime.now()
    album = Album(title=title, artist=artist, release_date=release_date, cover_url=cover_url, genre=genre, date_added=date_added)
    db.session.add(album)
    db.session.commit()

def create_review():
    summary = 'The Beatles\' final album is a masterpiece.'
    content = 'Abbey Road is the eleventh studio album by the English rock band the Beatles, released on 26 September 1969 by Apple Records. It was the final Beatles album to be released, and was also their last recording session together.'
    rating = 5
    reviewed_album = 1
    created_by = 1
    date_created = datetime.now()
    review = Review(summary=summary, content=content, rating=rating, reviewed_album=reviewed_album, created_by=created_by, date_created=date_created)
    db.session.add(review)
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

class MainTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
    def test_home_logged_out(self):
        """Test that the home page loads with sign in and join us buttons when logged out."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)
        self.assertIn(b'Join Us', response.data)

    def test_home_logged_in(self):
        """Test that the user is redirected to the all_earworms page 
        with browse, profile  and log out options visible when logged in."""
        create_user()
        login(self.app, 'test_user', 'password1234!')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log Out', response.data)
        self.assertIn(b'Profile', response.data)
        self.assertIn(b'Browse', response.data)

    def test_artist_view(self):
        """Test that the artist view page loads with the artist's name and bio."""
        create_artist()
        response = self.app.get('/artist/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The Beatles', response.data)
        self.assertIn(b'The Beatles were an English rock band formed in Liverpool in 1960.', response.data)

    def test_album_view(self):
        """Test that the album view page loads with the album's name, artist and release date."""
        create_artist()
        create_album()
        response = self.app.get('/album/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The Beatles', response.data)
        self.assertIn(b'Abbey Road', response.data)
        self.assertIn(b'26 September, 1969', response.data)

    def test_review_view(self):
        """Test that the review view page loads with the review's summary, content and rating."""
        create_user()
        create_artist()
        create_album()
        create_review()
        response = self.app.get('/review/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The Beatles&#39; final album is a masterpiece.', response.data)
        self.assertIn(b'Abbey Road is the eleventh studio album by the English rock band the Beatles, released on 26 September 1969 by Apple Records. It was the final Beatles album to be released, and was also their last recording session together.', response.data)
        self.assertIn(b'5', response.data)

    def test_all_earworms_view(self):
        """Test that the all earworms view page loads with the title and artist of each album."""
        create_artist()
        create_album()
        response = self.app.get('/all_earworms', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The Beatles', response.data)
        self.assertIn(b'Abbey Road', response.data)

    def test_album_detail_view(self):
        """Test that if there is a review for an album, it pulls through to the 
        album detail page with a summary, content and rating."""
        create_user()
        create_artist()
        create_album()
        create_review()
        response = self.app.get('/album/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The Beatles&#39; final album is a masterpiece.', response.data)
        self.assertIn(b'Abbey Road is the eleventh studio album by the English rock band the Beatles, released on 26 September 1969 by Apple Records. It was the final Beatles album to be released, and was also their last recording session together.', response.data)
        self.assertIn(b'5', response.data)

    def test_private_user_does_not_show(self):
        """Test that a private user does not show up in the browse page."""
        create_second_user()
        create_artist()
        create_album()
        create_review()
        response = self.app.get('/all_earworms', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'test_user2', response.data)

    def test_public_user_shows(self):
        """Test that a public user does show up in the browse page."""
        create_user()
        create_artist()
        create_album()
        create_review()
        response = self.app.get('/all_earworms', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_user', response.data)

    def test_user_profile_view(self):
        """Test that the user profile page loads with the user's username and bio."""
        create_user()
        response = self.app.get('/profile/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_user', response.data)
        self.assertIn(b'I was born in a small town in the middle of nowhere.', response.data)
