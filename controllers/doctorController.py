from models import db, Doctor, User

# ------------------- Get Doctor by User ID -------------------
def get_doctor_by_user_id(user_id):
    """
    Retrieve a doctor's profile using the linked user_id.
    """
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"success": False, "message": "Doctor not found."}
    return {"success": True, "doctor": doctor}


# ------------------- Update Doctor Profile -------------------
def update_doctor_profile(user_id, data):
    """
    Update doctor information fields such as name, specialization, contact.
    """
    try:
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return {"success": False, "message": "Doctor not found."}

        # Update provided fields only
        if "name" in data:
            doctor.name = data["name"]
        if "specialization" in data:
            doctor.specialization = data["specialization"]
        if "contact" in data:
            doctor.contact = data["contact"]

        db.session.commit()
        return {"success": True, "message": "Doctor profile updated successfully.", "doctor": doctor}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
