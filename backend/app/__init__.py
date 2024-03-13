import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_session import Session
import redis
from flask_sqlalchemy import SQLAlchemy
from .blueprints import register_blueprints
from prometheus_flask_exporter import PrometheusMetrics
from flask_jwt_extended import JWTManager
from .database import db
from .redis_client import redis_client

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

    # Database configuration
    DATABASE_URI = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Redis configuration
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url(app.config['REDIS_URL'])

    #JWT Configurations
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')  # Change this to a random secret key

    jwt = JWTManager(app)

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Session
    Session(app)

    # Initialize Redis client with app context
    redis_client.init_app(app)

    # Call the logging configuration function
    configure_logging(app)

    # Import models here to ensure they are known to Flask-SQLAlchemy
    from . import models

    # Register blueprints
    register_blueprints(app)

    # Initialize Prometheus metrics after registering blueprints
    PrometheusMetrics(app)


    return app