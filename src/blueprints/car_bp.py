"""
Cars Blueprint Module

Contains routes related to cars

Routes:

    url_prefix: '/cars'

    GET '/' : returns all the cars that exist in 'cars'

    GET '/me/' : returns all the user cars

    GET '/<string:make>/<string:model>' :  returns cars that match the given make and model

    GET '/<string:make>/' : returns cars that match the given make

    POST '/me/' :  add a new car. Adds to the cars entity first and then assigns to the user

    DELETE '/me/<int:user_car_id>' : delete a car from the user's car list

    DELETE '/<int:car_id>' : ADMIN ONLY: Admin can delete cars from the cars entity

    PUT/PATCH '/<int:car_id>' ADMIN ONLY: Admin can update a car in the cars entity
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.car import Car, CarSchema
from models.user_car import UserCar, UserCarSchema
from blueprints.auth_bp import verify_user

car_bp = Blueprint('car', __name__, url_prefix='/cars')

@car_bp.route('/')
@jwt_required()
def get_all_cars():
    """
    All cars view function

    This view function returns all the cars in the Cars table
    """
    # verify the user
    user = verify_user()
    if user:
        # select all from the cars table
        stmt = db.select(Car)
        cars = db.session.scalars(stmt).all()
        return CarSchema(many=True, exclude=['user_car']).dump(cars)
    return {"forbidden": "You must be logged in to access resource"}, 403

@car_bp.route('/<int:car_id>/')
@jwt_required()
def get_a_car(car_id):
    """
    A single car view function

    This view function returns a single car in the Cars table

    Variables:

            <car_id> (int)
    """
    # verify the user
    user = verify_user()
    if user:
        # select cars and filter by car_id
        stmt = db.select(Car).filter_by(id=car_id)
        car = db.session.scalar(stmt)
        if car:
            return CarSchema(exclude=['user_car']).dump(car)
        return {'not_found': "Car not found"}, 404
    return {"forbidden": "You must be logged in to access resource"}, 403


@car_bp.route('/<string:make>/<string:model>')
@jwt_required()
def get_cars_by_make_model(make, model):
    """
    Cars by Make and Model

    Returns cars that match the dynamic routes

    Variables:

            <make>  (str)

            <model>  (str)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # searching for cars using the .where() method, by model and make
    stmt = db.select(Car).where(
        db.and_(
            Car.make == make.capitalize(),
            Car.model == model.capitalize()
        )
    )
    cars = db.session.scalars(stmt).all()
    if cars:
        return CarSchema(many=True, exclude=['user_car']).dump(cars)
    return {'not_found': "Car make or model not found"}, 404


@car_bp.route('/<string:make>/')
@jwt_required()
def get_cars_by_make(make):
    """
    Cars by Make

    Returns cars that match the dynamic route

    Variables:

            <make>  (str)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # searching for cars using the .where() method, for the make
    stmt = db.select(Car).where(Car.make == make.capitalize())
    cars = db.session.scalars(stmt).all()
    if cars:
        return CarSchema(many=True, exclude=['user_car']).dump(cars)
    return {'not_found': "Car make not found"}, 404

# add a new car
@car_bp.route('/me/', methods=['POST'])
@jwt_required()
def add_new_car():
    """
    Add a new Car

    Allows the user to add a new car of their choice. The function first searches for
    the card that the user has sent through the body request.

    If the car exists in the 'cars' table, the car is added to the user's car list.

    If the car doesn't exist, the car is first added to the 'cars' table. The databse is
    queried again and the newly added car is selected.

    The car is then added to the user's car list

    Request body:

        required fields:

            {
                "make" : "car make",

                "model" : "car model",

                "model_trim" : "car model trim",

                "year" : "year car was made",

                "tank_size" : "car tank size"
            }
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # load the request using the Car schema
    car_info = CarSchema().load(request.json)
    # query the database to see if the car already exists
    stmt = db.select(Car).where(
        db.and_(
            Car.make == car_info['make'],
            Car.model == car_info['model'],
            Car.model_trim == car_info['model_trim'],
            Car.year == car_info['year'],
            Car.tank_size == car_info['tank_size']
        )
    )
    add_car = db.session.scalar(stmt)
    if not add_car:
        # add the car to the cars list if it doesn't exists
        new_car = Car(
            make= car_info['make'],
            model= car_info['model'],
            model_trim= car_info['model_trim'],
            year= car_info['year'],
            tank_size= car_info['tank_size']
        )
        # add and commit the car
        db.session.add(new_car)
        db.session.commit()
        # query the database again and select the newly added car
        new_stmt = db.select(Car).order_by(Car.id.desc())
        recent_car = db.session.scalars(new_stmt).first()
        # add the car to the user's cars list
        new_user_car = UserCar(
            user_id= get_jwt_identity(),
            car_id= recent_car.id
        )
        # add and commit the car to user cars
        db.session.add(new_user_car)
        db.session.commit()
        return UserCarSchema(exclude=['user_id']).dump(new_user_car)

    # check if user already has car
    stmt = db.select(UserCar).filter_by(
        user_id=get_jwt_identity()
    ).filter_by(
        car_id=add_car.id
    )
    existing_user_car = db.session.scalar(stmt)
    if add_car and not existing_user_car:
        # add the car to the user's cars list it user doesn't have the car in their list
        new_user_car = UserCar(
            user_id= get_jwt_identity(),
            car_id= add_car.id
        )
        # add and commit the car to user cars
        db.session.add(new_user_car)
        db.session.commit()
        return UserCarSchema(exclude=['user_id']).dump(new_user_car)


# get user cars
@car_bp.route('/me/')
@jwt_required()
def get_user_cars():
    """
    All user cars view function

    This view function returns all the user cars
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database and filter by the user id
    stmt = db.select(UserCar).filter_by(user_id=user.id)
    user_cars = db.session.scalars(stmt).all()
    if user_cars:
        return UserCarSchema(many=True, only=['id','car']).dump(user_cars)
    return {"not_found": "User has no cars added to their list"}, 404

# get user cars
@car_bp.route('/me/<int:car_id>/')
@jwt_required()
def get_user_car(car_id):
    """
    A user car view function

    This view function returns a user car
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database and filter by the user id and car id
    stmt = db.select(UserCar).filter_by(user_id=user.id).filter_by(id=car_id)
    user_car = db.session.scalar(stmt)
    if user_car:
        return UserCarSchema(only=['id','car']).dump(user_car)
    return {"not_found": "User car not found"}, 404


# delete user car
@car_bp.route('/me/<int:user_car_id>', methods=['DELETE'])
@jwt_required()
def delete_user_car(user_car_id):
    """
    Delete a user car view function

    Allows a user to delete a car from their list

    Variables:

            <user_car_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database to find user car
    stmt = db.select(UserCar).filter_by(
        user_id= user.id
    ).filter_by(
        id= user_car_id
    )
    user_car = db.session.scalars(stmt).first()
    if user_car:
        # delete and commit the selected car
        db.session.delete(user_car)
        db.session.commit()
        return {'deleted': 'removed car from user list'}
    return {'not_found': "User car not found"}, 404


# ADMIN ROUTES
# admin can delete car from the cars table
@car_bp.route('/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    """
    Delete a car view function

    Allows the admin user to delete a car from the cars table

    Variables:

            <car_id> (int)
    """
    # admin access
    admin = verify_user()
    if not admin.is_admin:
        return {"unauthorized" : "Admin access only"}, 401
    # query the database to find the car by the car id
    stmt = db.select(Car).filter_by(id= car_id)
    car = db.session.scalar(stmt)
    if car:
        # find in user cars as well and delete the user car record
        stmt = db.delete(UserCar).filter_by(car_id= car_id)
        db.session.execute(stmt)
        # delete car from cars table
        db.session.delete(car)
        db.session.commit()
        return {'admin_deleted': 'car successfully deleted'}
    return {'not_found': 'Car not found'}, 404


# admin can update car info in cars table
@car_bp.route('/<int:car_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_car_info(car_id):
    """
    Update a car view function

    Allows the admin user to update a car in the cars table

    Variables

            <car_id> (int)
    """
    # admin access
    admin = verify_user()
    if not admin.is_admin:
        return {"unauthorized" : "Admin access only"}, 401
    # query the database to find the car by the car id
    stmt = db.select(Car).filter_by(id= car_id)
    car = db.session.scalar(stmt)
    if car:
        # load the request body to car schema
        car_info = CarSchema().load(request.json)
        # update the car info
        car.make= car_info.get('make', car.make)
        car.model= car_info.get('model', car.model)
        car.model_trim= car_info.get('model_trim', car.model_trim)
        car.year= car_info.get('year', car.year)
        car.tank_size= car_info.get('tank_size', car.tank_size)
        # commit the update
        db.session.commit()
        return CarSchema(exclude=['user_car']).dump(car)
    return {'not_found': 'Car not found'}, 404
