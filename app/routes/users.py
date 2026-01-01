from flask import Blueprint, request, jsonify
from app.services.user_service import signup_user, login_user, get_user_by_id

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# List all users (for dev/testing)
@users_bp.route('/', methods=['GET'])
def list_users():
    # Optional: admin-only in production
    from app.services.user_service import get_all_users
    return jsonify(get_all_users())

# Signup endpoint
@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    required_fields = ['email', 'password', 'role', 'company', 'country']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = signup_user(data)
    if "error" in user:
        return jsonify(user), 400

    # Determine next step
    next_step = 'company_intake' if user['role'] == 'startup' else 'dashboard'

    return jsonify({
        "id": user['id'],
        "email": user['email'],
        "company": user['company'],
        "country": user['country'],
        "role": user['role'],
        "next_step": next_step
    }), 201

# Login endpoint
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

# Get user info by ID
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)
