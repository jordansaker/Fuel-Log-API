"""
Log Entries Blueprint Module

Contains routes related to log entries

Routes:

    url_prefix: '/logs'
"""
from datetime import datetime
from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.log import LogEntry, LogEntrySchema
from models.user_car import UserCar, UserCarSchema

log_bp = Blueprint('log', __name__, url_prefix='/logs')

# get user's log for selected car
@log_bp.route('/me/<int:car_id>/')
@jwt_required()
def get_log_entries(car_id):
    """
    Log Entries for car

    Get all the log entries for specified user car

    Variables:

            <car_id> (int)
    """
    # query the database for user car's id
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        # query the database and filter logs by user_car_id
        stmt = db.select(LogEntry).filter_by(user_car_id=user_car.id)
        log_entries = db.session.scalars(stmt).all()
        if log_entries:
            return LogEntrySchema(many=True).dump(log_entries)
        return {'msg': 'No log entries for user car'}
    abort(404, "User car not found")


# add a new log
@log_bp.route('/me/<int:car_id>/', methods=['POST'])
@jwt_required()
def add_log_entry(car_id):
    """
    Add Log Entry

    Add a log entry for the specified user car

    Variables:

            <car_id> (int)
    """
    # query the database for user car's id
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        # load the requeest body to the log entry schema
        log_entry_info = LogEntrySchema().load(request.json)
        # create a new log entry
        new_log_entry = LogEntry(
            current_odo= log_entry_info['current_odo'],
            fuel_quantity= log_entry_info['fuel_quantity'],
            fuel_price= log_entry_info['fuel_price'],
            date_added= datetime.now().timestamp(),
            user_car_id= car_id
        )
        # add and commit new log entry
        db.session.add(new_log_entry)
        db.session.commit()
        return LogEntrySchema(exclude=['user_trips']).dump(new_log_entry)
    abort(404, "User car not found")

# update a log entry
# delete a log entry
# calculate the average consumption
# calculate the trip cost
# expenditure summary
