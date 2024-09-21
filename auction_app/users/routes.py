"""Users Routes Module"""
from auction_app.users.forms import (RegestrationForm, LoginForm, 
                         UpdateAccountForm, RequestRestForm, RestPasswordForm)
from auction_app import db, bcrypt
from auction_app.users.utils import save_picture, send_reset_email
from auction_app.models import User, Auction
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions.auctions'))
    form = RegestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """Login Route"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions.auctions'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auctions.auctions'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    """Logout Route"""
    logout_user()
    return redirect(url_for('auctions.auctions'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_image_file.data:
            picture_file = save_picture(form.profile_image_file.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title="Profile",
                           image_file=image_file, form=form)

@users.route('/user/<string:username>', methods=['GET', 'POST'])
def user_auctions(username):
    """Auction List"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    auctions = Auction.query.filter_by(bid=user)\
        .order_by(Auction.date_posted.desc())\
        .paginate(page=page, per_page=6)
    return render_template('user_auctions.html', title="Home",
                           auctions=auctions, user=user)
    
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """Auction List"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions_.auctions'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
            flash('An Email has been sent with instructions to rest your password')
            return redirect(url_for('users.login'))
        except:
            flash("Failed to send a Reset token to Email", 'danger')
    return render_template('reset_request.html', title='Rest Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Auction List"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalide or expired token', 'warning')
        return redirect(url_for('users.rest_request'))
    form = RestPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your account has been updated! You are able to login now', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Rest Password', form=form)
