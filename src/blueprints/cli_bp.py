"""
CLI Blueprints

The following commands are run in the CLI. To invoke a command in the blue print:

       ``flask cli <command>``

Commands:

    ``create`` - create tables in the database

    ``drop`` - drop the existing tables in the database

    ``seed`` - seed the existing tables in the database
"""
from datetime import datetime
from flask import Blueprint
from models.user import User
from models.car import Car
from models.log import LogEntry
from models.user_car import UserCar
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
    print('Tables dropped')


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
    cars = [
        Car(
            make= "Ford",
            model= "Ranger",
            tank_size= 133
        ),
        Car(
            make= "Toyota",
            model= "Landcruiser",
            tank_size = 110
        )
    ]
    # add and commit the list
    db.session.add_all(cars)
    db.session.commit()
    # seed the user cars table
    user_cars = [
        UserCar(
            user= users[0],
            car= cars[1]
        ),
        UserCar(
            user= users[1],
            car= cars[0]
        )
    ]
    db.session.add_all(user_cars)
    db.session.commit()
    # seed the log entries table
    logs = [
        LogEntry(
            current_odo= 80100,
            fuel_quantity= 90,
            fuel_price= 1.86,
            date_added= datetime.now().timestamp(),
            avg_consumption= 8.25,
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 152462,
            fuel_quantity= 40,
            fuel_price= 1.90,
            date_added= datetime.now().timestamp(),
            avg_consumption= 5.75,
            usercar= user_cars[0]
        )
    ]
    # add and commit the list
    db.session.add_all(logs)
    db.session.commit()
    print('Tables seeded')
