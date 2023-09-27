from flask import Blueprint, request, jsonify
from models import User, db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from functools import wraps

auth_blueprint = Blueprint('auth', __name__)

def requires_roles(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user.role not in roles:
                return jsonify(message="Not authorized!"), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Generating JWT token for the authenticated user
        access_token = create_access_token(identity=user.user_id)
        return jsonify({'message': 'Logged in successfully!', 'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials!'}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # TODO: Implement the logout functionality, e.g. revoking the JWT token
    pass

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    # TODO: Implement password reset logic
    pass
