"""Form Module"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateTimeLocalField, 
                     TextAreaField, DecimalField)
from wtforms.validators import DataRequired, Length

class CreateAuctionForm(FlaskForm):
    """Create Auction Class"""
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    item_image_file = FileField('Auction Image', validators=[FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    initial_bid = DecimalField('Initial Bid', validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date')
    submit = SubmitField("Create Auction")
class PlaceBidForm(FlaskForm):
    """Place Bid"""
    bid_amount = DecimalField('Place Bid', validators=[DataRequired()])
    submit = SubmitField("Place Bid")
    