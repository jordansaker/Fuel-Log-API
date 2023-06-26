"""
Cars Model and Schema

This module contains the Car model and CarSchema classes

The Car Model contains the following attributes:

    id, make, model, model_trim, year, tank_size
"""
from marshmallow import fields
from marshmallow.validate import Regexp
from init import db, ma

class Car(db.Model):
    """
    The Car model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        make (str), model (str), model_trim (str), year (int), tank_size (int) 
    """

    __tablename__ = 'cars'
    # set unique constraints
    __table_args__ = (db.UniqueConstraint("make", "model", "model_trim"),)
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    model_trim = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer)
    tank_size = db.Column(db.Integer)
    # relationships to foreign key in other table (not model defined attributes)
    user_car = db.relationship('UserCar', backref='car')


class CarSchema(ma.Schema):
    """
    Car model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = (id', 'make', 'model', 'model_trim', 'year', 'tank_size', 'user_car')

    The field ``user_car`` is a nested field related to the UserCar Model
    """
    user_car = fields.Nested('UserCarSchema', exclude=['car'])
    # validate the data for each attribute
    make = fields.String(
        required=True,
        validate=Regexp('^[A-Z][a-zA-Z0-9 ]+$', error='Must capitalise the name')
    )
    model = fields.String(
        required=True,
        validate=Regexp('^[A-Z][a-zA-Z0-9 ]+$', error='Must capitalise the name')
    )
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'make', 'model', 'model_trim', 'year', 'tank_size', 'user_car')
        ordered = True
