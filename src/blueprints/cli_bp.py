"""
CLI Blueprints

The following commands are run in the CLI. To invoke a command in the blue print:

       ``flask cli <command>``

Commands:

    ``create`` - create tables in the database

    ``drop`` - drop the existing tables in the database

    ``seed`` - seed the existing tables in the database
"""
from flask import Blueprint
from models.user import User
from init import db, bcrypt

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

@cli_bp.cli.command('seed')
def seed_tables():
    """
    Seed the existing tables in the database
    """
    # seed the users table
    users = [
        User(
            first_name= "John",
            last_name= "Smith",
            email= "john.smith@test.com",
            password= bcrypt.generate_password_hash('password123').decode('utf8')
        ),
        User(
            first_name= "William",
            last_name= "Thomas",
            email= "will.thomas@gmail.com",
            password= bcrypt.generate_password_hash('thisIsapassword').decode('utf8')
        )
    ]
    # add and commit the list
    db.session.add_all(users)
    db.session.commit()
    # seed the cars table
    print('Tables seeded')
