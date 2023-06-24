"""
Log Entries Blueprint Module

Contains routes related to log entries

Routes:

    url_prefix: '/cars'
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from init import db
from models.log import LogEntry, LogEntrySchema

log_bp = Blueprint('log', __name__, url_prefix='/logs')

# get user's log
@log_bp.route('/')
@jwt_required()
def get_log_entries():
    """
    """
    # query the database for user's log entries
    stmt = db.select(LogEntry)
    logs = db.session.scalars(stmt).all()
    return LogEntrySchema(many=True).dump(logs)
