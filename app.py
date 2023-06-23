from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['SECRET_KEY'] = 'your-secret-key'

# In-memory user storage (replace with your database implementation)
users = []
auctions = []

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
    if any(user['username'] == username or user['email'] == email for user in users):
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create user object
    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }

    # Store user data (replace with your database operation)
    users.append(user)

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = next((user for user in users if user['username'] == username), None)

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check password match
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate access token (you can use Flask-JWT or another library for this)
    # Include additional data in the token if needed (e.g., user ID, role)
    access_token = generate_access_token(user['username'])

    return jsonify({'access_token': access_token}), 200


# Utility function to generate access token
def generate_access_token(username):
    payload = {'username': username}
    access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return access_token.decode('utf-8')

bids = []

# Utility function to find auction by ID
def find_auction_by_id(auction_id):
    return next((auction for auction in auctions if auction['id'] == auction_id), None)

# Utility function to find highest bid for an auction
def find_highest_bid(auction_id):
    auction_bids = [bid for bid in bids if bid['auction_id'] == auction_id]
    if auction_bids:
        return max(auction_bids, key=lambda bid: bid['amount'])
    else:
        return None

@app.route('/api/auctions', methods=['POST'])
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
    auction = {
        'id': len(auctions) + 1,
        'title': title,
        'description': description,
        'initial_bid': initial_bid,
        'end_date': end_date
    }

    # Store auction data (replace with your database operation)
    auctions.append(auction)

    return jsonify({'message': 'Auction created successfully'}), 201

@app.route('/api/auctions/<int:auction_id>/bids', methods=['POST'])
def place_bid(auction_id):
    data = request.get_json()
    user_id = data.get('user_id')
    bid_amount = data.get('bid_amount')

    auction = find_auction_by_id(auction_id)
    if not auction:
        return jsonify({'error': 'Auction not found'}), 404

    highest_bid = find_highest_bid(auction_id)

    if not bid_amount or bid_amount <= auction['initial_bid']:
        return jsonify({'error': 'Invalid bid amount'}), 400

    if highest_bid and bid_amount <= highest_bid['amount']:
        return jsonify({'error': 'Bid amount must be higher than the current highest bid'}), 400

    bid = {
        'auction_id': auction_id,
        'user_id': user_id,
        'amount': bid_amount
    }

    bids.append(bid)

    return jsonify({'message': 'Bid placed successfully'}), 201
if __name__ == '__main__':
    app.run()
