"""
Users Model and Schema

This module contains the Log Entry model and LogEntrySchema classes

The Log Entry Model contains the following attributes:

    id, current_odo, fuel_quantity, fuel_price,
    
    date_added, avg_consumption, user_car_id 
"""
from datetime import datetime
from marshmallow import fields
from marshmallow.validate import Range
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
                    'fuel_price', 'date_added', 'user_car')
    """
    usercar = fields.Nested('UserCarSchema', exclude=['logs'])
    current_odo = fields.Integer(
        required=True,
        validate=Range(0)
    )
    fuel_quantity = fields.Integer(
        required=True,
        validate=Range(1)
    )
    fuel_price = fields.Float(
        required=True,
        validate=Range(0.01)
    )
    
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'current_odo',
                  'fuel_quantity', 'fuel_price', 
                    'date_added', 'usercar')
        ordered = True

class ExpenditureSchema(ma.Schema):
    """
    Expenditure schema for the expenditure route.

    Used to validate the date format that is being sent in the POST request
    """
    from_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    to_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('from_date', 'to_date')
        ordered = True
        dateformat = '%Y-%m-%d'

class ExpenditureCompareSchema(ma.Schema):
    """
    Compare Expenditures for 2 different time periods
    """
    from_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    to_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    compare_from_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    compare_to_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('from_date', 'to_date', 'compare_to_date', 'compare_from_date')
        ordered = True
        dateformat = '%Y-%m-%d'
