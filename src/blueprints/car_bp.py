"""
Cars Blueprint Module

Contains routes related to cars

Routes:

    url_prefix: '/cars'

    GET '/' : returns all the cars that exist in 'cars'

    GET '/me/' : returns all the user cars

    GET '/<make>/<model>' :  returns cars that match the given make and model

    GET '/<make>/' : returns cars that match the given make

    POST '/me/' :  add a new car    
"""
from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.car import Car, CarSchema
from models.user_car import UserCar, UserCarSchema

car_bp = Blueprint('car', __name__, url_prefix='/cars')

@car_bp.route('/')
def get_all_cars():
    """
    All cars view function

    This view function returns all the cars in the Cars table
    """
    # statement to query the database
    stmt = db.select(Car)
    cars = db.session.scalars(stmt).all()
    return CarSchema(many=True, exclude=['user_car']).dump(cars)


@car_bp.route('/<string:make>/<string:model>')
def get_cars_by_make_model(make, model):
    """
    Cars by Make and Model

    Returns cars that match the dynamic routes

    Variables:

        <make>  (str)

        <model>  (str)
    """
    # statement to query the database, searching for cars using the .where() method
    stmt = db.select(Car).where(
        db.and_(
            Car.make == make.capitalize(),
            Car.model == model.capitalize()
        )
    )
    cars = db.session.scalars(stmt).all()
    if cars:
        return CarSchema(many=True, exclude=['user_car']).dump(cars)
    abort(404, description='Car make or model not found')


@car_bp.route('/<string:make>/')
def get_cars_by_make(make):
    """
    Cars by Make

    Returns cars that match the dynamic route

    Variables:

        <make>  (str)
    """
    # statement to query the database, searching for cars using the .where() method
    stmt = db.select(Car).where(Car.make == make.capitalize())
    cars = db.session.scalars(stmt).all()
    if cars:
        return CarSchema(many=True, exclude=['user_car']).dump(cars)
    abort(404, description='Car make not found')

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
    # load the request using the Car schema
    car_info = CarSchema().load(request.json)
    # query the database to see if the car exists
    stmt = db.select(Car).where(
        db.and_(
            Car.make == car_info['make'],
            Car.model == car_info['model'],
            Car.model_trim == car_info['model_trim'],
            Car.year == car_info['year'],
            Car.tank_size == car_info['tank_size']
        )
    )
    car = db.session.scalar(stmt)
    if not car:
        # add the car to the cars list
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
            car_id= recent_car['id']
        )
        # add and commit the car to user cars
        db.session.add(new_user_car)
        db.session.commit()
        return UserCarSchema(exclude=['user_id']).dump(new_user_car)

    # return {"msg": car.id}
    if car:
        # add the car to the user's cars list
        new_user_car = UserCar(
            user_id= get_jwt_identity(),
            car_id= car.id
        )
        # add and commit the car to user cars
        db.session.add(new_user_car)
        db.session.commit()
        return UserCarSchema(exclude=['id', 'user']).dump(new_user_car)
