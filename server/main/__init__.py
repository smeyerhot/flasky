"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()

def create_app():
    """Construct the core application. (flask-app-factory)"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    
    with app.app_context():
        from main.users import users_blueprint
        app.register_blueprint(users_blueprint)
        # from . import routes  # Import routes
        db.create_all()  # Create database tables for our data models

        return app