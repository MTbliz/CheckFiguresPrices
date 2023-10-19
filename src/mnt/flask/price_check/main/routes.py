from price_check.main import bp
from flask import render_template
from price_check.figures.figures_service import filter_all_columns_by_value


@bp.route('/')
def det_page():
    return render_template('base.html')

@bp.route('/home')
def home_page():
    return render_template('base.html')

@bp.route('/market')
def market_page():
    return render_template('market.html')


@bp.route('/test')
def test():
    values = filter_all_columns_by_value(4)
    return str(values)





