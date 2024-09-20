from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)
@main.route("/")
def landing_page():
    """Landing Page route"""
    is_landing_page = True  # Set the flag for landing page
    return render_template('index.html', is_landing_page=is_landing_page)
