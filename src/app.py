'''Fuel Log API app
\nThis module creates a Flask app instance through OrJSONProvider.'''
from os import environ
from flask import Flask
from flask.json.provider import JSONProvider
from sqlalchemy.exc import IntegrityError
import orjson
from init import db, ma, jwt, bcrypt
from blueprints.auth_bp import auth_bp
from blueprints.cli_bp import cli_bp
from blueprints.car_bp import car_bp


class OrJSONProvider(JSONProvider):
    '''Class to use the JSON provider. This will allow schema fields to be ordered.'''
    def dumps(self, obj, *, option=None):
        '''Function for the dumps method'''
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC
        return orjson.dumps(obj).decode()
    def loads(self, s):
        '''Function for the loads method'''
        return orjson.loads(s)

def create_app():
    '''Function to create the flask app. Function creates an instance of Flask.'''
    # to use the JSON provider class, the Flask class
    # will be assigned and instance of the MyFlask Class
    class MyFlask(Flask):
        '''Assigning the OrJSONProvider to be used to create app instance.'''
        json_provider_class = OrJSONProvider

    # create the app instance
    app = MyFlask(__name__)
    # config the app setting the database URI and JWT secrect key
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
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
    # handle errors
    @app.errorhandler(401)
    def unauthorised(err):
        """
        Handle unauthorised codes passed to the flask abort() function

        ``err`` contains the error JSON response
        """
        return {'error': str(err)}, 401


    @app.errorhandler(404)
    def not_found(err):
        """
        Handle not found codes passed to the flask abort() function

        ``err`` contains the error JSON response
        """
        return {'error': str(err)}, 404


    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400


    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        return {'error': err}


    return app
