"""Authentication Blueprint

Contains routes related to user authentication.

Routes:

    /login  - 

    /register - 
"""
from datetime import timedelta
from flask import Blueprint, request, abort
from flask_jwt_extended import create_access_token
from init import bcrypt, db
from models.user import User, UserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def user_register():
    """
    User register view function

    Let's a new user register to use the API

    request body:

        required fields:

            {
                "email": "new user email",
                
                "password": "new user password",

                "first_name": "user first name",
                
                "last_name": "user last name"
            }
    """
    # sanitise the request body
    user_info = UserSchema().load(request.json)
    # create new user model instance with data
    new_user = User(
        first_name= user_info['first_name'],
        last_name= user_info['last_name'],
        email= user_info['email'],
        password= bcrypt.generate_password_hash(user_info['password']).decode('utf8')
    )
    # add and commit the new user
    db.session.add(new_user)
    db.session.commit()
    # return the user info and success message
    return {
            "msg": "Successfully created new user",
            "user_info": UserSchema(exclude=['password']).dump(new_user)
            }, 201


@auth_bp.route('/login', methods=['POST'])
def user_login():
    """
    User login view function

    Takes the post body and authenticates the user

    request body:

        required fields:

            {
                "email": "registered user email",

                "password": "registered user password"
            }
    """
    # find the user in the database
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # check if user exists
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # give user access token, token created using flask_jwt_extended
        token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=120))
        return {"token": token, "user": UserSchema(exclude=['password', 'reviews']).dump(user)}
    abort(401, description='Invalid email address or password')
