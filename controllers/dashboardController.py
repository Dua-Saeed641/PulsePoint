from models import db, Doctor, Patient, Appointment
from flask_login import current_user

def get_patient_dashboard(user_id):
    """
    Show patient's full profile along with upcoming and past appointments stats.
    """
    # Fetch patient info using user_id
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"success": False, "message": "Patient not found."}

    # Fetch appointments
    upcoming = Appointment.query.filter_by(patient_id=patient.id, status='upcoming').all()
    past = Appointment.query.filter_by(patient_id=patient.id, status='completed').all()

    # Prepare dashboard data
    data = {
        "role": "patient",
        "profile": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "contact": patient.contact,
            "address": patient.address,
            "email": patient.user.email if patient.user else None
        },
        "stats": {
            "upcoming_appointments": len(upcoming),
            "past_appointments": len(past)
        }
    }

    return {"success": True, "data": data}


# ------------------------ DOCTOR DASHBOARD ------------------------
def get_doctor_dashboard(doctor_id):
    """
    Show doctor-specific dashboard details:
    - Basic profile info
    - Total appointments
    - Unique patients count
    - Breakdown of upcoming and completed appointments
    """
    # Fetch doctor info
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return {"success": False, "message": "Doctor not found."}

    # Fetch all appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()

    # Categorize appointments
    upcoming = [a for a in appointments if a.status == 'upcoming']
    completed = [a for a in appointments if a.status == 'completed']

    # Collect unique patients seen
    unique_patients = len({a.patient_id for a in appointments})

    # Prepare response data
    data = {
        "role": "doctor",
        "profile": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "contact": doctor.contact,
            "email": doctor.user.email if doctor.user else None
        },
        "stats": {
            "total_appointments": len(appointments),
            "upcoming_appointments": len(upcoming),
            "completed_appointments": len(completed),
            "unique_patients": unique_patients
        }
    }

    return {"success": True, "data": data}
