from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, ma, limiter, cache 
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp
from .parts import parts_bp
from .config import DevConfig, TestingConfig

def create_app(config_name="DevConfig"):
    app = Flask(__name__)

    # Load the appropriate config
    if config_name == "TestingConfig":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevConfig)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Disable limiter during tests
    if not app.config.get("RATELIMIT_ENABLED", True):
        limiter.enabled = False

    limiter.init_app(app)
    cache.init_app(app)


    # Register blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(parts_bp, url_prefix="/parts")

    # Swagger UI
    swagger_url = "/docs"
    api_url = "/static/swagger.yaml"

    swaggerui_bp = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={"app_name": "Mechanic Shop API"}
    )
    app.register_blueprint(swaggerui_bp, url_prefix=swagger_url)
    
    # # Auto-create tables
    # with app.app_context():
    #     db.create_all()
    #     print("Database ready")

    return app
