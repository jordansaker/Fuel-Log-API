'''Fuel Log API app
This module creates a Flask app instance through OrJSONProvider.'''
from flask import Flask
from flask.json.provider import JSONProvider
from os import environ
import orjson
from config import Config
from init import db, ma, jwt, bcrypt


class OrJSONProvider(JSONProvider):
    '''Class to use the JSON provider. This will allow schema fields to be ordered'''
    def dumps(self, obj, *, option=None):
        '''Function for the dumps method'''
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC
        return orjson.dumps(obj).decode()
    def loads(self, s):
        '''Function for the loads method'''
        return orjson.loads(s)

def create_app():
    '''Function to create the flask app. Function creates an instance of Flask'''
    # to use the JSON provider class, the Flask class
    # will be assigned and instance of the MyFlask Class
    class MyFlask(Flask):
        '''Assigning the OrJSONProvider to be used to create app instance'''
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
    return app
