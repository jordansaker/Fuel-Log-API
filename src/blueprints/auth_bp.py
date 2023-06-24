"""Authentication Blueprint

Contains routes related to user authentication.

Routes:

    /login  -  allows existing user to authenticate, returing an access token

    /register -  allows a user to register
"""
from datetime import timedelta
from flask import Blueprint, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
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
            "user_info": UserSchema(exclude=['password', 'is_admin']).dump(new_user)
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
        return {
                "token": token, 
                "user": UserSchema(exclude=['id', 'password', 'is_admin']).dump(user)
               }
    abort(401, description='Invalid email address or password')


def admin_access():
    """
    Admin Access Function

    Allows only the admin user to access the route 
    this function is called in. Function is placed in the view function
    """
    # get the user's identity
    user_id = get_jwt_identity()
    # query the database and check if the user is_admin
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    print(user.is_admin)
    if not user.is_admin:
        abort(401, description='admin access only')
