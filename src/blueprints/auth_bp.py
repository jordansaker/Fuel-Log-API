'''Authentication Blueprint

Contains routes related to user authentication.

Routes:

    /login  - 

    /register - 
'''
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def user_login():
    '''User login view function. Takes the post body and authenticates the user'''
    return {'msg': 'hello'}, 200
