'''Configure the Flask App.
This module gets the JWT Secret Key and DB URI configuration and connection
string using the Config class'''
from os import environ

class Config(object):
    '''Config class for the Flask app.
    Uses the envrion.get() method to get the JWT key and DB URI'''
    # access the .env file and get the JWT Key
    JWT_KEY = environ.get("JWT_KEY")
    # access the .env file and get the DB URI
    DB_URI =  environ.get('DB_URI')
