from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from controllers.dashboardController import get_doctor_dashboard
from controllers.doctorController import update_doctor_profile, get_doctor_by_user_id

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/doctor/dashboard', methods=['GET'])
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        return jsonify({"error": "Unauthorized access"}), 403

    # Get doctor object using user_id
    result = get_doctor_by_user_id(current_user.id)
    if not result['success']:
        return jsonify({"error": result['message']}), 404

    doctor = result['doctor']

    data = get_doctor_dashboard(doctor.id)  # use Doctor ID, not User ID

    if not data['success']:
        return jsonify({"error": data['message']}), 404

    return jsonify(data), 200


# ------------------- Update Doctor Profile -------------------
@doctor_bp.route('/doctor/update', methods=['PUT'])
@login_required
def update_doctor_info():
    if current_user.role != 'doctor':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json() or request.form
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = update_doctor_profile(current_user.id, data)
    if not result['success']:
        return jsonify({"error": result['message']}), 400

    doctor = result['doctor']
    return jsonify({
        "message": "Profile updated successfully!",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "contact": doctor.contact
        }
    }), 200
