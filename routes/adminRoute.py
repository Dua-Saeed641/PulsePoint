from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from controllers.adminController import (
    get_admin_dashboard, 
    create_patient, get_patient, update_patient, delete_patient, search_patients,
    create_doctor, get_doctor, update_doctor, delete_doctor, search_doctors,
    create_department, get_department, update_department,delete_department,search_departments
)
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# -------------------- Admin Access Decorator --------------------
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"success": False, "message": "Access denied. Admins only."}), 403
        return fn(*args, **kwargs)
    return wrapper

# -------------------- Dashboard --------------------
@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def admin_dashboard():
    data = get_admin_dashboard()
    return jsonify({"success": True, "data": data}), 200

# -------------------- Patient CRUD + Search --------------------
@admin_bp.route('/patient', methods=['POST'])
@login_required
@admin_required
def add_patient():
    data = request.json
    patient = create_patient(
        name=data.get('name'),
        age=data.get('age'),
        gender=data.get('gender'),
        contact=data.get('contact'),
        address=data.get('address'),
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify({"success": True, "patient_id": patient.id}), 201

@admin_bp.route('/patient/<int:patient_id>', methods=['GET'])
@login_required
@admin_required
def get_patient_by_id(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        return jsonify({"success": False, "message": "Patient not found"}), 404
    return jsonify({"success": True, "data": {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact,
        "address": patient.address,
        "email": patient.user.email if patient.user else None
    }}), 200

@admin_bp.route('/patient/<int:patient_id>', methods=['PUT'])
@login_required
@admin_required
def update_patient_by_id(patient_id):
    data = request.json
    patient = update_patient(patient_id, **data)
    if not patient:
        return jsonify({"success": False, "message": "Patient not found"}), 404
    return jsonify({"success": True, "message": "Patient updated"}), 200

@admin_bp.route('/patient/<int:patient_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_patient_by_id(patient_id):
    success = delete_patient(patient_id)
    if not success:
        return jsonify({"success": False, "message": "Patient not found"}), 404
    return jsonify({"success": True, "message": "Patient deleted"}), 200

@admin_bp.route('/patient/search', methods=['GET'])
@login_required
@admin_required
def search_patient_route():
    query = request.args.get('q', '')
    patients = search_patients(query)
    results = [{
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "gender": p.gender,
        "contact": p.contact,
        "email": p.user.email if p.user else None
    } for p in patients]
    return jsonify({"success": True, "results": results}), 200

# -------------------- Doctor CRUD + Search --------------------
@admin_bp.route('/doctor', methods=['POST'])
@login_required
@admin_required
def add_doctor():
    data = request.json
    doctor = create_doctor(
        name=data.get('name'),
        specialization=data.get('specialization'),
        contact=data.get('contact'),
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify({"success": True, "doctor_id": doctor.id}), 201

@admin_bp.route('/doctor/<int:doctor_id>', methods=['GET'])
@login_required
@admin_required
def get_doctor_by_id(doctor_id):
    doctor = get_doctor(doctor_id)
    if not doctor:
        return jsonify({"success": False, "message": "Doctor not found"}), 404
    return jsonify({"success": True, "data": {
        "id": doctor.id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "contact": doctor.contact,
        "email": doctor.user.email if doctor.user else None
    }}), 200

@admin_bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
@login_required
@admin_required
def update_doctor_by_id(doctor_id):
    data = request.json
    doctor = update_doctor(doctor_id, **data)
    if not doctor:
        return jsonify({"success": False, "message": "Doctor not found"}), 404
    return jsonify({"success": True, "message": "Doctor updated"}), 200

@admin_bp.route('/doctor/<int:doctor_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_doctor_by_id(doctor_id):
    success = delete_doctor(doctor_id)
    if not success:
        return jsonify({"success": False, "message": "Doctor not found"}), 404
    return jsonify({"success": True, "message": "Doctor deleted"}), 200

@admin_bp.route('/doctor/search', methods=['GET'])
@login_required
@admin_required
def search_doctor_route():
    query = request.args.get('q', '')
    doctors = search_doctors(query)
    results = [{
        "id": d.id,
        "name": d.name,
        "specialization": d.specialization,
        "contact": d.contact,
        "email": d.user.email if d.user else None
    } for d in doctors]
    return jsonify({"success": True, "results": results}), 200

# -------------------- Department CRUD + Search --------------------
@admin_bp.route('/department', methods=['POST'])
@login_required
@admin_required
def add_department():
    data = request.json
    dept = create_department(
        name=data.get('name'),
        description=data.get('description')
    )
    return jsonify({"success": True, "department_id": dept.id}), 201


@admin_bp.route('/department/<int:dept_id>', methods=['GET'])
@login_required
@admin_required
def get_department_by_id(dept_id):
    dept = get_department(dept_id)
    if not dept:
        return jsonify({"success": False, "message": "Department not found"}), 404
    return jsonify({"success": True, "data": {
        "id": dept.id,
        "name": dept.name,
        "description": dept.description
    }}), 200


@admin_bp.route('/department/<int:dept_id>', methods=['PUT'])
@login_required
@admin_required
def update_department_by_id(dept_id):
    data = request.json
    dept = update_department(dept_id, **data)
    if not dept:
        return jsonify({"success": False, "message": "Department not found"}), 404
    return jsonify({"success": True, "message": "Department updated"}), 200


@admin_bp.route('/department/<int:dept_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_department_by_id(dept_id):
    success = delete_department(dept_id)
    if not success:
        return jsonify({"success": False, "message": "Department not found"}), 404
    return jsonify({"success": True, "message": "Department deleted"}), 200


@admin_bp.route('/department/search', methods=['GET'])
@login_required
@admin_required
def search_department_route():
    query = request.args.get('q', '')
    depts = search_departments(query)
    results = [{
        "id": d.id,
        "name": d.name,
        "description": d.description
    } for d in depts]
    return jsonify({"success": True, "results": results}), 200
