from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

def create_app():
    """Factory pattern to create a Flask app instance"""
    app = Flask(__name__)

    # Configuration
    # Using environment variables for sensitive information is a best practice
    DATABASE_URI = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import models here to ensure they are known to Flask-SQLAlchemy
    from . import models


    return app