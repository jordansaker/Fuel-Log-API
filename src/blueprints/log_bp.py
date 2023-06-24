"""
Log Entries Blueprint Module

Contains routes related to log entries

Routes:
"""
from flask import Blueprint

log_bp = Blueprint('log', __name__, url_prefix='/log')