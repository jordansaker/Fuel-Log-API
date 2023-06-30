"""Authentication Blueprint

Contains routes related to user authentication.

Routes:

    POST '/login'  -  allows existing user to authenticate, returing an access token

    POST '/register' -  allows a user to register

    DELETE '/me/<int:user_id>/delete/' - ADMIN and user only: delete a user account
"""
from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import bcrypt, db
from models.user import User, UserSchema
from models.user_car import UserCar

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
        first_name= user_info.get('first_name', None),
        last_name= user_info.get('last_name', None),
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
    # find the user in the database using the email value from the body request
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # check if user exists
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # give user access token, token created using flask_jwt_extended
        token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=120))
        return {
                "token": token, 
                "user": UserSchema(exclude=['id', 'password']).dump(user)
               }
    return {"invalid_user_info" : "Invalid email address or password"}, 401

# Admin only access
@auth_bp.route('/users/')
@jwt_required()
def get_users():
    """
    Allows the admin to get a list of entire users
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in or registered"}, 403
    if user.is_admin:
        # select all users from the users table
        stmt = db.select(User)
        users = db.session.scalars(stmt).all()
        return UserSchema(many=True, exclude=['password', 'cars']).dump(users)
    return {"unauthorized" : "Admin access only"}, 401


@auth_bp.route('/me/<int:user_id>/delete/', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete a user

    Delete a user record. A user can delete their record or the admin can delete all records

    Variables:

            <user_id> (int)    
    """
    # verify the user
    admin_delete_user = verify_user()
    if not admin_delete_user:
        return {"forbidden": "You must be logged in or registered"}, 403

    if admin_delete_user:
        # if the user is the correct user and not the admin
        if admin_delete_user.id == user_id and not admin_delete_user.is_admin:
            db.session.delete(admin_delete_user)
            db.session.commit()
            return {'deleted': 'user successfully deleted'}
        # users can't delete other users only admin
        if not admin_delete_user.is_admin:
            return {"unauthorized" : "Admin access only"}, 401
        # find the user for admin to delete
        user_to_delete = User.query.filter_by(id=user_id).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        return {'admin_deleted': 'user successfully deleted'}
    return {"invalid_user" : "User not found"}, 404

def verify_user_car(car_id):
    """
    Verify that the user making the request is allowed to access the
    response

    Variables:

            <car_id> (int)

    Returns the user object
    """
    # get a user object based on the car id and return to calling function
    stmt = db.select(UserCar).filter_by(user_id=get_jwt_identity()).filter_by(id=car_id)
    user = db.session.scalar(stmt)
    return user

def verify_user():
    """
    Verify that user exists using the JWT token linked to the user ID
    """
    # get a user object and return to the calling function
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    return user
