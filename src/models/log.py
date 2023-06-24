"""
Users Model and Schema

This module contains the Log Entry model and LogEntrySchema classes

The Log Entry Model contains the following attributes:

    id, current_odo, fuel_quantity, fuel_price,
    
    date_added, avg_consumption, user_car_id 
"""
from datetime import datetime
from marshmallow import fields
from init import db, ma


class LogEntry(db.Model):
    """
    The Car model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        current_odo (int), fuel_quantity (int), fuel_price (float), 
        
        date_added (datetime), avg_consumption (float), user_car_id (int) 
    """
    __tablename__ = 'log_entries'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    current_odo = db.Column(db.Integer, nullable=False)
    fuel_quantity = db.Column(db.Integer, nullable=False)
    fuel_price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.BigInteger, default=datetime.now().timestamp())
    avg_consumption = db.Column(db.Float, nullable=False)
    # Foreign Keys
    user_car_id = db.Column(
                            db.Integer,
                            db.ForeignKey('user_cars.id', ondelete='cascade'),
                            nullable=True
                        )


class LogEntrySchema(ma.Schema):
    """
    Log Entry model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'current_odo', 'fuel_quantity', 
                    'fuel_price', 'date_added', 'avg_consumption', 'user_car')
    """
    usercar = fields.Nested('UserCarSchema', exclude=['logs'])
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'current_odo',
                  'fuel_quantity', 'fuel_price', 
                    'date_added', 'avg_consumption', 'usercar')
        ordered = True
