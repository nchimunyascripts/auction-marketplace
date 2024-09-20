"""Form Module"""
from flask_wtf import FlaskForm
from auction_app.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, EmailField, SubmitField, BooleanField,
                     PasswordField)
from wtforms.validators import DataRequired, Email,EqualTo, Length, ValidationError
from flask_login import current_user

class RegestrationForm(FlaskForm):
    """Register Class"""
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")
    def validate_username(self, username):
        """Validates Username"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User with this username exists.\
                Please choose a different username!')
    def validate_email(self, email):
        "Validates Emails"
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('An Account with this email already exists. Please login!')
class LoginForm(FlaskForm):
    """Login Form"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign Up")
class UpdateAccountForm(FlaskForm):
    """Update Form"""
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    profile_image_file = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update Account")
    def validate_username(self, username):
        """Validates Username"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('User with this username exists.\
                    Please choose a different username!')
    def validate_email(self, email):
        """Validates Emails"""
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('An Account with this email already exists. Please login!')

class RequestRestForm(FlaskForm):
    """Request Reset"""
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        """Validates Email"""
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. You must register first!')
class RestPasswordForm(FlaskForm):
    """Reset Password"""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    