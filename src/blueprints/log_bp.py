"""
Log Entries Blueprint Module

Contains routes related to log entries

Routes:

    url_prefix: '/logs'
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.log import LogEntry, LogEntrySchema
from models.user_car import UserCar, UserCarSchema

log_bp = Blueprint('log', __name__, url_prefix='/logs')

# get user's log for selected car
@log_bp.route('/me/<int:car_id>')
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
        return LogEntrySchema(many=True).dump(log_entries)
