from flask import Flask
from .db import db, migrate
from .routes.planet_routes import planets_bp
from .models import planet
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        app.config.update(config)
   
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(planets_bp)
    return app
