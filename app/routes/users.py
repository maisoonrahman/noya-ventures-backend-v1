from flask import Blueprint, request, jsonify
from app.services.user_service import signup_user, login_user, get_user_by_id, get_all_users

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


# -----------------------
# List users (dev only)
# -----------------------
@users_bp.route('/', methods=['GET'])
def list_users():
    return jsonify(get_all_users())


# -----------------------
# Signup
# -----------------------
@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    required_fields = ['email', 'password', 'role', 'country']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = signup_user(data)
    if "error" in user:
        return jsonify(user), 400

    next_step = 'company_intake' if user['role'] == 'startup' else 'dashboard'

    return jsonify({
        "id": user['id'],
        "email": user['email'],
        "role": user['role'],
        "country": user['country'],
        "next_step": next_step
    }), 201


# -----------------------
# Login
# -----------------------
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password required"}), 400

    user = login_user(data)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    next_step = 'company_intake' if user['role'] == 'startup' else 'dashboard'
    user['next_step'] = next_step

    return jsonify(user)


# -----------------------
# Get user by ID
# -----------------------
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)
