from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
import jwt
from models import db, User, Auction, Bid
from datetime import datetime
import secrets

secret_key = secrets.token_hex(32)

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def landing_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate input data
        if not username or not email or not password:
            return render_template('register.html', error='Invalid input')

        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error='Username or email already exists')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user object
        user = User(username=username, email=email, password=hashed_password)

        # Store user data
        db.session.add(user)
        db.session.commit()

        return render_template('login.html', message='User registered successfully')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template('login.html', error='Invalid username or password')

        # Check password match
        if not bcrypt.check_password_hash(user.password, password):
            return render_template('login.html', error='Invalid username or password')

        # Generate access token
        access_token = generate_access_token(user.username)

        # Render the template with access_token as a parameter
        return render_template('profile.html', access_token=access_token)

    return render_template('login.html')


@app.route('/auctions', methods=['GET', 'POST'])
def auctions():
    if request.method == 'POST':
        data = request.form
        title = data.get('title')
        description = data.get('description')
        initial_bid = data.get('initial_bid')
        end_date = data.get('end_date')

        end_date = datetime.fromisoformat(end_date.replace('T', ' '))
        # Validate input data
        if not title or not initial_bid or not end_date:
            return render_template('create_auction.html', error='Invalid input')

        # Create auction object
        auction = Auction(title=title, description=description, initial_bid=initial_bid, end_date=end_date)
        # Store auction data
        db.session.add(auction)
        db.session.commit()

        return render_template('create_auction.html', message='Auction created successfully')

    return render_template('create_auction.html')

@app.route('/auctions/<int:auction_id>/bids', methods=['POST'])
def place_bid(auction_id):
    data = request.form
    user_id = data.get('user_id')
    bid_amount = data.get('bid_amount')

    auction = Auction.query.get(auction_id)
    if not auction:
        return render_template('place_bid.html', error='Auction not found')

    highest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.amount.desc()).first()

    if not bid_amount or bid_amount <= auction.initial_bid:
        return render_template('place_bid.html', error='Invalid bid amount')

    if highest_bid and bid_amount <= highest_bid.amount:
        return render_template('place_bid.html', error='Bid amount must be higher than the current highest bid')

    # Create bid object
    bid = Bid(auction_id=auction_id, user_id=user_id, amount=bid_amount)

    # Store bid data
    db.session.add(bid)
    db.session.commit()

    return render_template('place_bid.html', message='Bid placed successfully')

@app.route('/auctions/<int:auction_id>', methods=['GET', 'POST'])
def update_auction(auction_id):
    auction = Auction.query.get(auction_id)
    if not auction:
        return render_template('update_auction.html', error='Auction not found')

    if request.method == 'POST':
        data = request.form
        auction.title = data['title']
        auction.description = data['description']
        auction.end_date = data['end_date']

        db.session.commit()

        return render_template('update_auction.html', auction=auction, message='Auction updated successfully')

    return render_template('update_auction.html', auction=auction)

@app.route('/auctions/<int:auction_id>/delete', methods=['POST'])
def delete_auction(auction_id):
    auction = Auction.query.get(auction_id)
    if not auction:
        return render_template('delete_auction.html', error='Auction not found')

    db.session.delete(auction)
    db.session.commit()

    return render_template('delete_auction.html', message='Auction deleted successfully')

# Utility function to generate access token
def generate_access_token(username):
    payload = {'username': username}
    access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return access_token

if __name__ == '__main__':
    app.run(debug=True)