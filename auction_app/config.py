"""Config"""
import os

class Config:
    """Config"""
    SECRET_KEY = 'f4ea1665ef538be8a39d5a649be81f10'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///auction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
