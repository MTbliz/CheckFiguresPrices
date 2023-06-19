from flask import Blueprint

bp = Blueprint('figures', __name__)

from price_check.figures import routes