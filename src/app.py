'''
Fuel Log API app

This module creates a Flask app instance.
'''
from os import environ
from flask import Flask
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from init import db, ma, jwt, bcrypt
from blueprints.auth_bp import auth_bp
from blueprints.cli_bp import cli_bp
from blueprints.car_bp import car_bp
from blueprints.log_bp import log_bp

def create_app():
    '''Function to create the flask app. Function creates an instance of Flask.'''
    # create the app instance
    app = Flask(__name__)
    # config the app setting the database URI and JWT secrect key
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    app.json.sort_keys = False
    # app.config.from_object(Config)
    # initialise the database instance from the init.py file
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cli_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(log_bp)
    # handle errors
    @app.errorhandler(400)
    def bad_request():
        return {'bad_request': 'No JSON object Found in request body'}, 400


    @app.errorhandler(IntegrityError)
    def integrity_error():
        return {'integrity_error': 'Data already exists in database'}, 400

    @app.errorhandler(UnsupportedMediaType)
    def unsupported_request(err):
        return {'error': err.description}

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'valiadtion_error': err.messages}, 400

    return app
