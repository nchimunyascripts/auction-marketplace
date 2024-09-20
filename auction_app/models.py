"""Models Module"""
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from auction_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """Load user with id"""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User Table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    auctions = db.relationship('Auction', backref='bid', lazy=True)
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.load(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Auction(db.Model):
    """Auction Table"""
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='placeholder.jpg')
    initial_bid = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f"Auction('{self.title}', '{self.date_posted}')"
