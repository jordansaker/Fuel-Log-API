"""
Intialising the Flask app.

This Module creates instances of SQLAlchemy, Marshmallow, JWTManager, Bcrypt.

The instances are assigned to db, ma, jwt, and bcrypt respectively
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()
