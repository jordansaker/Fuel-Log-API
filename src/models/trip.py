"""
Trip Model and Schema

This module contains the Trip model and TripSchema classes.

The Trip model contains the following attributes:

    id, fuel_price, car_id (Foreign Key)
"""
from marshmallow import fields
from init import db, ma

class Trip(db.Model):
    """
    The Usercar model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        fuel_price (float), distance (int)
    """
    __tablename__ = 'user_trips'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    fuel_price = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    # foreign keys
    user_car_id = db.Column(db.Integer,
                        db.ForeignKey('user_cars.id', ondelete='cascade'),
                        nullable=False
                    )


class TripSchema(ma.Schema):
    """
    Trip model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'fuel_price', 'distance', 'user_car')

    """
    usercar = fields.Nested('UserCarSchema')
    
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'fuel_price', 'distance', 'usercar', 'user_car_id')
        ordered = True
