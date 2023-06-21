"""
Cars Model and Schema

This module contains the Car model and CarSchema classes

The Car Model contains the following attributes:

    id, make, model, tank_size
"""
from init import db, ma

class Car(db.Model):
    """
    The Car model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        make, model, tank_size 
    """

    __tablename__ = 'cars'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String())
    model = db.Column(db.String())
    tank_size = db.Column(db.String())


class CarSchema(ma.Schema):
    """
    Car model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'make', 'model', 'tank_size')
    """
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'make', 'model', 'tank_size')
        ordered = True
