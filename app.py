from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    initial_bid = db.Column(db.Float, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Auction {self.title}>'


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Bid {self.amount}>'


db.create_all()


@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input data
    if not username or not email or not password:
        return jsonify({'error': 'Invalid input'}), 400

    # Check if username or email already exists
    existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create user object
    user = User(username=username, email=email, password=hashed_password)

    # Store user data
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check password match
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate access token
    access_token = generate_access_token(user.username)

    return jsonify({'access_token': access_token}), 200


# Utility function to generate access token
def generate_access_token(username):
    payload = {'username': username}
    access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return access_token.decode('utf-8')

@app.route('/api/auctions',

 methods=['POST'])
def create_auction():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    initial_bid = data.get('initial_bid')
    end_date = data.get('end_date')

    # Validate input data
    if not title or not initial_bid or not end_date:
        return jsonify({'error': 'Invalid input'}), 400

    # Create auction object
    auction = Auction(title=title, description=description, initial_bid=initial_bid, end_date=end_date)

    # Store auction data
    db.session.add(auction)
    db.session.commit()

    return jsonify({'message': 'Auction created successfully'}), 201


@app.route('/api/auctions/<int:auction_id>/bids', methods=['POST'])
def place_bid(auction_id):
    data = request.get_json()
    user_id = data.get('user_id')
    bid_amount = data.get('bid_amount')

    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({'error': 'Auction not found'}), 404

    highest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.amount.desc()).first()

    if not bid_amount or bid_amount <= auction.initial_bid:
        return jsonify({'error': 'Invalid bid amount'}), 400

    if highest_bid and bid_amount <= highest_bid.amount:
        return jsonify({'error': 'Bid amount must be higher than the current highest bid'}), 400

    # Create bid object
    bid = Bid(auction_id=auction_id, user_id=user_id, amount=bid_amount)

    # Store bid data
    db.session.add(bid)
    db.session.commit()

    return jsonify({'message': 'Bid placed successfully'}), 201


@app.route('/api/auctions/<int:auction_id>', methods=['PUT'])
def update_auction(auction_id):
    data = request.json

    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({'error': 'Auction not found'}), 404

    auction.title = data['title']
    auction.description = data['description']
    auction.end_date = data['end_date']

    db.session.commit()

    return jsonify({'message': 'Auction updated successfully'}), 200


@app.route('/api/auctions/<int:auction_id>', methods=['DELETE'])
def delete_auction(auction_id):
    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({'error': 'Auction not found'}), 404

    db.session.delete(auction)
    db.session.commit()

    return jsonify({'message': 'Auction deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
