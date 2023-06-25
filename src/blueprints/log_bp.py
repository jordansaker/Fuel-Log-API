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
from models.car import CarSchema

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
@log_bp.route('/me/<int:car_id>/trip/calculator/<int:distance>/<float:fuel_price>')
@jwt_required()
def calculate_avg_consuption(car_id, distance, fuel_price):
    """
    Trip calculator and Average Consumption

    Calculates the average fuel consumption. Queries the database for the last 2 log entries
    and calculates the distance between fill ups.

    Calculates how much fuel was used from previous fills.

    Average will only be calculated once there is more than 2 log entries for the user car.

    The trip calculator relies on the average. Once the average can be calculated, the trip
    cost will be calculated based on the average.

    Variables:

            <car_id> (int)

            <distance> (int) distance of the trip

            <fuel_price> (float)
    """
    # query the database for user car's id
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        # filter the log entries using the user car id, order by date added
        stmt = db.select(LogEntry).filter_by(
                                    user_car_id=car_id
                                ).order_by(LogEntry.date_added.desc())
        log_entries = db.session.scalars(stmt).all()
        if len(log_entries) > 2:
            # last 2 entries are in list position's 0 and 1
            # calculate the distance travelled from one fill up
            # gather as many data points for distance travelled
            distance_travelled = log_entries[0].current_odo - log_entries[-2].current_odo
            # average fuel consumed from last fill up
            # is isn't the real average consumption as the fuel left in the tank isn't recorded
            # fuel total
            total_fuel = 0
            for index in range(1, len(log_entries) - 1):
                total_fuel += log_entries[index].fuel_quantity
            # average consumption
            avg_consumption = (total_fuel) / (distance_travelled / 100)
            # esitmated fuel needed for trip
            trip_fuel = avg_consumption * (distance / 100)
            # estimated trip cost
            trip_cost = trip_fuel * fuel_price
            return {
                'avg_consumption': f"{format(avg_consumption, '.2f')} L/100km",
                'estimated_trip_fuel': f"{format(trip_fuel, '.2f')} L",
                'esitmated_trip_cost': f"${format(trip_cost, '.2f')}",
                'car': CarSchema(exclude=['id', 'user_car']).dump(user_car.car)
            }
        return {
            'calculation_error': 'unable to calculate average consumption due to number of log entries present',
            'log_entries_required': 'Require more than 2 log entries for user car'
        }
    abort(404, "User car not found")


# expenditure summary
