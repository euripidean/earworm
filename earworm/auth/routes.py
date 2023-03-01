from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from earworm.extensions import app, db, bcrypt

from earworm.auth.forms import SignUpForm, LoginForm, UserUpdateForm
from earworm.models import User, Review, Artist


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up for a user account."""
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'), 
            avatar_url=form.avatar_url.data, 
            public=form.public.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('Users/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next = request.args.get('next')
        if next:
            flash('You are now logged in.', 'success')
            return redirect(next)
        else:
            flash('You are now logged in.', 'success')
            return redirect(url_for('main.all_earworms'))
    return render_template('Users/login.html', form=form)

@auth.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    """Show a user's profile page."""
    user = User.query.get(user_id)
    if user.public == False and user.id != current_user.id:
        flash('This user has a private profile.', 'danger')
        return redirect(url_for('main.all_earworms'))
    liked_artists = user.liked_artists
    return render_template('Users/profile.html', user=user, reviews=user.reviews_written, liked_artists=liked_artists)

@auth.route('/edit_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    """Edit a user's profile."""
    user = User.query.get(user_id)
    form = UserUpdateForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.avatar_url = form.avatar_url.data
        user.bio = form.bio.data
        user.public = form.public.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile', user_id=user.id))
    return render_template('Users/edit_profile.html', form=form, user=user)

@auth.route('/logout')
@login_required
def logout():
    """Log out a user."""
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.homepage'))

@auth.route('/all_users')
def all_users():
    """Show all users on a page."""
    users = User.query.all()
    return render_template('Users/all_users.html', users=users)


@auth.route('/delete/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_profile(user_id):
    """Delete a user's profile."""
    user = User.query.get(user_id)
    user.liked_artists = []
    reviews = Review.query.filter_by(created_by=user.id).all()
    for review in reviews:
        db.session.delete(review)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.homepage'))


