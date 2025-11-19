from flask import Flask
from .extensions import db, ma
from . import models  # make sure models are imported
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"

    # Init extensions
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    # Auto-create tables
    with app.app_context():
        db.create_all()
        print("Database ready")

    return app
