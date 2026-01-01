from flask import Blueprint, request, jsonify
from app.services.startup_service import save_intake_step, get_startup_by_user

startups_bp = Blueprint('startups', __name__, url_prefix='/api/startups')

# Step-based intake form (steps 1-4)
@startups_bp.route('/intake/<int:step>', methods=['POST'])
def intake_step(step):
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    result = save_intake_step(user_id, step, data)
    return jsonify(result)

# Dashboard data for startup
@startups_bp.route('/dashboard/<int:user_id>', methods=['GET'])
def dashboard(user_id):
    startup = get_startup_by_user(user_id)
    if not startup:
        return jsonify({"error": "Startup data not found"}), 404
    return jsonify({"startup": startup})
