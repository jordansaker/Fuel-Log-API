"""
Users Model and Schema

This module contains the User model and UserSchema Classes

The User Model contains the following attributes:

    id, first_name, last_name, email, password
"""
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp
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
    first_name = db.Column(db.String(), default='null')
    last_name = db.Column(db.String(), default='null')
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    # relationships to foreign key in other table (not model defined attributes)
    cars = db.relationship('UserCar', backref='user')


class UserSchema(ma.Schema):
    """
    User model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'cars')

    The field ``cars`` is a nested field related to the UserCar Model
    """
    cars = fields.List(fields.Nested(
                'UserCarSchema', 
                exclude=['id', 'logs', 'user_id']
            ))
    password = fields.String(
        required=True,
        validate=Length(min=8),
    )
    first_name = fields.String(
        validate=Regexp('^[a-zA-Z]+$', error="Must only contain letters")
    )
    last_name = fields.String(
        validate=Regexp('^[a-zA-Z]+$', error="Must only contain letters")
    )
    email = fields.Email(required=True)
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'email', 'first_name', 'last_name', 'cars', 'password')
        ordered = True
