from auction_app.auctions.forms import CreateAuctionForm
from auction_app import db
from auction_app.models import Auction
from auction_app.auctions.utils import save_item_picture
from flask import Blueprint, redirect, url_for, flash, render_template, request, abort
from flask_login import current_user, login_required

auction_ = Blueprint('auctions', __name__)

@auction_.route('/auctions', methods=['GET', 'POST'])
def auctions():
    """Auction List"""
    page = request.args.get('page', 1, type=int)
    auctions = Auction.query.order_by(Auction.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('list_auctions.html', title="Home", auctions=auctions)

@auction_.route('/new_auction', methods=['GET', 'POST'])
@login_required
def new_auction():
    """Auction List"""
    form = CreateAuctionForm()
    if form.validate_on_submit():
        # item_picture = save_item_picture(form.item_image_file.data)
        auction = Auction(title=form.title.data, description=form.description.data,
                          initial_bid=form.initial_bid.data, 
                          end_date=form.end_date.data, bid=current_user)
        db.session.add(auction)
        db.session.commit()
        # print(auction)
        flash('Your auction hass been created!', 'success')
        return redirect(url_for('auctions.auctions'))
    return render_template('create_auction.html', title="New Auction",
                           form=form, legend="Create Auction")
@auction_.route('/auctions/<int:auction_id>', methods=['GET', 'POST'])
def auction(auction_id):
    """Auction List"""
    auction = Auction.query.get_or_404(auction_id)
    image_file = url_for('static', filename='item_pics/' + auction.image_file)
    return render_template('auction.html', title=auction.title, auction=auction, image_file=image_file)
@auction_.route('/auctions/<int:auction_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('auctions.auction', auction_id=auction.id))
    elif request.method == 'GET':
        form.title.data = auction.title
        form.description.data = auction.description
        form.initial_bid.data = auction.initial_bid
        form.end_date.data = auction.end_date
    return render_template('create_auction.html', title='Update Auction', form=form, legend="Update Auction")
@auction_.route('/auctions/<int:auction_id>/delete', methods=['POST'])
@login_required
def delete_auction(auction_id):
    """Auction List"""
    auction = Auction.query.get_or_404(auction_id)
    if auction.bid != current_user:
        abort(403)
    db.session.delete(auction)
    db.session.commit()
    flash("Auction has been Deleted!", "success")
    return redirect(url_for('auctions.auctions'))
