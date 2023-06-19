from flask import Flask
from config import Config
from price_check.extensions import db
from price_check.main import bp as main_bp
from price_check.figures import bp as figures_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)

    # Register blueprints here

    app.register_blueprint(main_bp)
    app.register_blueprint(figures_bp)

    from price_check import routes

    return app