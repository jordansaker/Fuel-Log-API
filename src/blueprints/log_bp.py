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
        return LogEntrySchema().dump(new_log_entry)
    abort(404, "User car not found")

# update a log entry
@log_bp.route('/me/<int:car_id>/<int:log_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_log_entry(car_id, log_id):
    """
    Update Log Entry

    Update an existing log entry for the specified user car

    Variables:

            <car_id> (int)

            <log_id> (int)
    """
    # query the database for user car's id
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        # search for the log entry
        stmt = db.select(LogEntry).filter_by(id=log_id)
        log_entry = db.session.scalar(stmt)
        if log_entry:
            # load the reponse to the Log Entry Schema
            log_info = LogEntrySchema().load(request.json)
            # update the log entry fields
            log_entry.current_odo = log_info.get('current_odo', log_entry.current_odo)
            log_entry.fuel_quantity = log_info.get('fuel_quantity', log_entry.fuel_quantity)
            log_entry.fuel_price = log_info.get('fuel_price', log_entry.fuel_price)
            log_entry.user_car_id = car_id
            # commit the update
            db.session.commit()
            return LogEntrySchema().dump(log_entry)
        abort(404, "Log entry not found")
    abort(404, "User car not found")

# delete a log entry
@log_bp.route('/me/<int:car_id>/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log_entry(car_id, log_id):
    """
    Delete Log Entry

    Delete and existing log entry for the specified user car

    Variables:

            <car_id> (int)

            <log_id> (int)
    """
    # query the database for user car's id
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        # search for the log entry
        stmt = db.select(LogEntry).filter_by(id=log_id)
        log_entry = db.session.scalar(stmt)
        if log_entry:
            # delete the log and commit
            db.session.delete(log_entry)
            db.session.commit()
            return {'msg': 'Log entry deleted from user car'}
        abort(404, "Log entry not found")
    abort(404, "User car not found")
        

# calculate the average consumption
# calculate the trip cost
# expenditure summary
