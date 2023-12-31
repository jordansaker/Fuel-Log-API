"""
CLI Blueprints

The following commands are run in the CLI. To invoke a command in the blue print:

       ``flask cli <command>``

Commands:

    ``create`` - create tables in the database

    ``drop`` - drop the existing tables in the database

    ``seed`` - seed the existing tables in the database
"""
from datetime import datetime, timezone, timedelta
from time import timezone as tz
from flask import Blueprint
from models.user import User
from models.car import Car
from models.log import LogEntry
from models.user_car import UserCar
from models.trip import Trip
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
            email= "fuellogadmin@fuellogapi.com",
            password= bcrypt.generate_password_hash('admin1234').decode('utf8'),
            is_admin= True
        ),
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
            model_trim= 'Raptor',
            year= 2022,
            tank_size= 80
        ),
        Car(
            make= "Toyota",
            model= "Landcruiser",
            model_trim= '100 series',
            year= 2004,
            tank_size = 110
        )
    ]
    # add and commit the list
    db.session.add_all(cars)
    db.session.commit()
    # seed the user cars table
    user_cars = [
        UserCar(
            user= users[1],
            car= cars[1]
        ),
        UserCar(
            user= users[2],
            car= cars[0]
        )
    ]
    db.session.add_all(user_cars)
    db.session.commit()
    # seed the log entries table
    logs = [
        LogEntry(
            current_odo= 80100,
            fuel_quantity= 80,
            fuel_price= 1.86,
            date_added= datetime(
                        2023, 5, 7, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 152462,
            fuel_quantity= 40,
            fuel_price= 1.90,
            date_added= datetime.now(
                        tz=timezone(timedelta(hours=( tz/3600.0 * -1 )))
                    ).timestamp(),
            usercar= user_cars[0]
        ),
        LogEntry(
            current_odo= 80800,
            fuel_quantity= 80,
            fuel_price= 1.95,
            date_added= datetime(
                        2023, 5, 15, 9, 30, 00, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 81600,
            fuel_quantity= 80,
            fuel_price= 1.89,
            date_added= datetime(
                        2023, 5, 23, 18, 30, 00, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 81900,
            fuel_quantity= 40,
            fuel_price= 1.82,
            date_added= datetime(
                        2023, 5, 27, 19, 30, 00, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 82400,
            fuel_quantity= 60,
            fuel_price= 1.86,
            date_added= datetime(
                        2023, 6, 4, 12, 30, 00, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        ),
        LogEntry(
            current_odo= 83100,
            fuel_quantity= 80,
            fuel_price= 1.98,
            date_added= datetime(
                        2023, 6, 15, 10, 30, 00, tzinfo=datetime.now().astimezone().tzinfo
                    ).timestamp(),
            usercar= user_cars[1]
        )
    ]
    # add and commit the list
    db.session.add_all(logs)
    db.session.commit()
    # seed the user trips table
    user_trips = [
        Trip(
            fuel_price= 1.87,
            distance= 100,
            usercar= user_cars[0]
        ),
        Trip(
            fuel_price= 1.90,
            distance= 400,
            usercar= user_cars[1]
        ),
        Trip(
            fuel_price= 1.95,
            distance= 800,
            usercar= user_cars[1]
        )
    ]
    db.session.add_all(user_trips)
    db.session.commit()
    print('Tables seeded')
