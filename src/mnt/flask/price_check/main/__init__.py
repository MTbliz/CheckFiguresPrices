from flask import Blueprint

bp = Blueprint('main', __name__)

from price_check.main import routes