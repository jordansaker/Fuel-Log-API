"""
UserCar Model and Schema

This module contains the UserCar model and UserCarSchema classes. This
model represents the joining table for Users and Cars

The UserCar model contains the following attributes:

    id, user_id (Foreign Key), car_id (Foreign Key)
"""
from marshmallow import fields
from init import db, ma

class UserCar(db.Model):
    """
    The Usercar model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        user_id (int), car_id (int)
    """
    __tablename__ = 'user_cars'
    # model atributes
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    # relationships to foreign key in other table (not model defined attributes)
    log_entry = db.relationship('LogEntry', backref='usercar')
    user_trip = db.relationship('Trip', backref='usercar')


class UserCarSchema(ma.Schema):
    """
    User Car model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'user_id', 'car_id', 'log_entry')

    The field ``log_entry`` is a nested field related to the LogEntry Model

    The field ``user_trip`` is a nested field related to the Tripy Model 
    """
    # nested fields
    log_entry = fields.List(fields.Nested('LogEntrySchema'))
    user = fields.Nested('UserSchema', exclude=['_is_admin', 'user_car'])
    car = fields.Nested('CarSchema', exclude=['id', 'user_car'])
    user_trip = fields.List(fields.Nested('TripSchema', exclude=['user_car']))
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'user', 'car', 'log_entry', 'user_trip')
        ordered = True
