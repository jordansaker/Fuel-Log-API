"""CLI blueprints
The following commands are run in the CLI. To invoke a command in the blue print:

       ``flask cli <command>``

Commands:

    ``create`` - create tables in the database

    ``drop`` - drop the existing tables in the database

    ``seed`` - seed the existing tables in the database
"""
from flask import Blueprint
from models.user import User
from init import db

cli_bp = Blueprint('cli', __name__)

@cli_bp.cli.command('create')
def create_tables():
    '''Create the tables in the database using the defined models'''
    db.create_all()
    print('Tables created')

@cli_bp.cli.command('drop')
def drop_tables():
    '''Drop the existing tables in the database'''
    db.drop_all()
