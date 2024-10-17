from flask_httpauth import HTTPTokenAuth
from app.utils.utils import decode_token
from app.models import User 
from app.database import db
from flask import request, jsonify
from app import app
from functools import wraps


token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    user_id = decode_token(token)
    if user_id is not None:
        return User.query.get(user_id)
    return None

@token_auth.error_handler
def token_auth_error(status_code):
    return jsonify({'error': 'Unauthorized access'}), status_code

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token_auth.verify_token(token):
            return token_auth_error(401)
        return func(*args, **kwargs)
    return decorated_function

@token_auth.get_user_roles 
def get_roles (user):
    return [user.role.role_name]

@app.route('/protected', methods=['GET'])
@login_required
def protected_route():
    return jsonify({'message': 'This route is protected by JWT authentication'})