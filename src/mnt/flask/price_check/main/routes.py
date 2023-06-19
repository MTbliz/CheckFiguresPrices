from price_check.main import bp
from flask import render_template


@bp.route('/')
def det_page():
    return render_template('base.html')

@bp.route('/home')
def home_page():
    return render_template('base.html')

@bp.route('/market')
def market_page():
    return render_template('market.html')




