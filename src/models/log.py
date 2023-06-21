"""
Users Model and Schema

This module contains the Log Entry model and LogEntrySchema classes

The Log Entry Model contains the following attributes:

    id, current_odo, fuel_quantity, fuel_price, date_added, avg_consumption 
"""
from init import db, ma


class LogEntry(db.Model):
    """
    The Car model representing the cars entity in the database.

    Creates a model instance of the database instance.

    Attributes:

        current_odo (int), fuel_quantity (int), fuel_price (int), avg_consumption (int) 
    """
    __tablename__ = 'log_entries'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    current_odo = db.Column(db.Integer, nullable=False)
    fuel_quantity = db.Column(db.Integer, nullable=False)
    fuel_price = db.Column(db.Decimal, nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now(), nullable=False)
    avg_consumption = db.Column(db.Integer, nullable=False)


class LogEntrySchema(ma.Schema):
    """
    Log Entry model Schema

    The data for each field is validated in this class before being
    committed to the database.

    The fields are defined in a tuple in the Meta subclass

    class Meta:
        fields = ('id', 'current_odo', 'fuel_quantity', 'fuel_price', 'date_added', 'avg_consumption')
    """
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('id', 'current_odo', 'fuel_quantity', 'fuel_price', 'date_added', 'avg_consumption')
        ordered = True