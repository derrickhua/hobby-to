import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .blueprints import register_blueprints
from prometheus_flask_exporter import PrometheusMetrics


# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

def configure_logging(app):
    # Configure basic logging to stdout
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    
    # File logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/myflaskapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask application startup')

def create_app():
    """Factory pattern to create a Flask app instance"""
    app = Flask(__name__)

    DATABASE_URI = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Call the logging configuration function
    configure_logging(app)

    # Import models here to ensure they are known to Flask-SQLAlchemy
    from . import models

    # Register blueprints
    register_blueprints(app)

    # Initialize Prometheus metrics after registering blueprints
    PrometheusMetrics(app)


    return app