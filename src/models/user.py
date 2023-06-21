"""
Users Model and Schema

This module contains the User model and UserSchema Classes

The User Model contains the following attributes:

    id, first_name, last_name, email, password
"""
from init import db, ma

class User(db.Model):
    """
    The User model representing the Users entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        first_name (str), last_name (str), email (str), password (str)
    """
    __tablename__ = 'users'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)


class UserSchema(ma.Schema):
    """
    User model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
    """
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        ordered = True
