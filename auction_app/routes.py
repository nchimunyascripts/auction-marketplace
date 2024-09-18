import secrets
import os
from flask import flash, render_template, redirect, url_for, request, abort
from auction_app.forms import RegestrationForm, LoginForm, UpdateAccountForm, CreateAuctionForm, RequestRestForm, RestPasswordForm
from auction_app.models import User, Auction
from auction_app import app, db, bcrypt, mail
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
@app.route("/")
def landing_page():
    """Landing Page route"""
    is_landing_page = True  # Set the flag for landing page
    return render_template('index.html', is_landing_page=is_landing_page)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions'))
    form = RegestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Route"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auctions'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    """Logout Route"""
    logout_user()
    return redirect(url_for('auctions'))

def save_picture(form_picture):
    """Save Image"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def profile(username):
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
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    user = User.query.filter_by(username=username).first_or_404()
    auctions = Auction.query.filter_by(bid=user)\
        .order_by(Auction.date_posted.desc())
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title="Profile",
                           image_file=image_file, form=form, auctions=auctions)
      
@app.route('/auctions', methods=['GET', 'POST'])
def auctions():
    """Auction List"""
    page = request.args.get('page', 1, type=int)
    auctions = Auction.query.order_by(Auction.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('list_auctions.html', title="Home", auctions=auctions)
def save_item_picture(form_picture):
    """Save Image"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/item_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
@app.route('/new_auction', methods=['GET', 'POST'])
@login_required
def new_auction():
    """Auction List"""
    form = CreateAuctionForm()
    if form.validate_on_submit():
        item_picture = save_item_picture(form.item_image_file.data)
        auction = Auction(title=form.title.data, description=form.description.data,
                          initial_bid=form.initial_bid.data, image_file=item_picture,
                          end_date=form.end_date.data, bid=current_user)
        db.session.add(auction)
        db.session.commit()
        print(auction)
        flash('Your auction hass been created!', 'success')
        return redirect(url_for('auctions'))
    return render_template('create_auction.html', title="New Auction", 
                           form=form, legend="Create Auction")
@app.route('/auctions/<int:auction_id>', methods=['GET', 'POST'])
def auction(auction_id):
    """Auction List"""
    auction = Auction.query.get_or_404(auction_id)
    image_file = url_for('static', filename='item_pics/' + auction.image_file)
    return render_template('auction.html', title=auction.title, auction=auction, image_file=image_file)
@app.route('/auctions/<int:auction_id>/update', methods=['GET', 'POST'])
@login_required
def update_auction(auction_id):
    """Auction List"""
    auction = Auction.query.get_or_404(auction_id)
    if auction.bid != current_user:
        abort(403)
    form = CreateAuctionForm()
    if form.validate_on_submit():
        auction.title = form.title.data
        auction.description = form.description.data
        auction.initial_bid = form.initial_bid.data
        auction.end_date = form.end_date.data
        db.session.commit()
        flash('Auction has been updated!', 'success')
        return redirect(url_for('auction', auction_id=auction.id))
    elif request.method == 'GET':
        form.title.data = auction.title
        form.description.data = auction.description
        form.initial_bid.data = auction.initial_bid
        form.end_date.data = auction.end_date
    return render_template('create_auction.html', title='Update Auction', form=form, legend="Update Auction")

@app.route('/auctions/<int:auction_id>/delete', methods=['POST'])
@login_required
def delete_auction(auction_id):
    """Auction List"""
    auction = Auction.query.get_or_404(auction_id)
    if auction.bid != current_user:
        abort(403)
    db.session.delete(auction)
    db.session.commit()
    flash("Auction has been Deleted!", "success")
    return redirect(url_for('auctions'))
@app.route('/user/<string:username>', methods=['GET', 'POST'])
def user_auctions(username):
    """Auction List"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    auctions = Auction.query.filter_by(bid=user)\
        .order_by(Auction.date_posted.desc())\
        .paginate(page=page, per_page=6)
    return render_template('user_auctions.html', title="Home",
                           auctions=auctions, user=user)
def send_reset_email(user):
    """Reset Password"""
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then Simply ignore this email.
"""
    mail.send(msg)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """Auction List"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
            flash('An Email has been sent with instructions to rest your password')
            return redirect(url_for('login'))
        except:
            flash("Failed to send a Reset token to Email", 'danger')
    return render_template('reset_request.html', title='Rest Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Auction List"""
    if current_user.is_authenticated:
        return redirect(url_for('auctions'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalide or expired token', 'warning')
        return redirect(url_for('rest_request'))
    form = RestPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your account has been updated! You are able to login now', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Rest Password', form=form)
