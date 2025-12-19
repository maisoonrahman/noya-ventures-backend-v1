from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/', methods=['GET'])
def list_users():
    # placeholder response
    return jsonify([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
