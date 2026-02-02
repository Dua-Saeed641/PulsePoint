from models import db, User, Patient, Doctor, Appointment, Department
from werkzeug.security import generate_password_hash


# ------------------------ ADMIN DASHBOARD ------------------------
def get_admin_dashboard():
    """
    Return summary for admin dashboard:
    - total doctors
    - total patients
    - total appointments
    - active patients (patients with upcoming appointments)
    - upcoming appointments count
    - completed appointments count
    """
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    upcoming_appointments = Appointment.query.filter_by(status='upcoming').count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    
    # Active patients: patients with at least one upcoming appointment
    active_patient_ids = {a.patient_id for a in Appointment.query.filter_by(status='upcoming').all()}
    active_patients_count = len(active_patient_ids)

    return {
        "role": "admin",
        "stats": {
            "total_doctors": total_doctors,
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "upcoming_appointments": upcoming_appointments,
            "completed_appointments": completed_appointments,
            "active_patients": active_patients_count
        }
    }

# ------------------------ PATIENT CRUD ------------------------
def create_patient(name, age, gender, contact, address, email, password):
    """
    Create a new patient along with user account.
    """

    user = User(email=email, password_hash=generate_password_hash(password), role='patient')
    db.session.add(user)
    db.session.commit()

    patient = Patient(user_id=user.id, name=name, age=age, gender=gender, contact=contact, address=address)
    db.session.add(patient)
    db.session.commit()

    return patient

def get_patient(patient_id):
    return Patient.query.get(patient_id)

def update_patient(patient_id, **kwargs):
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    for key, value in kwargs.items():
        if hasattr(patient, key):
            setattr(patient, key, value)
    db.session.commit()
    return patient

def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return False
    db.session.delete(patient)
    db.session.commit()
    return True

def search_patients(query):
    """
    Search patients by name, contact, or email.
    """
    return Patient.query.join(User).filter(
        (Patient.name.ilike(f"%{query}%")) |
        (Patient.contact.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    ).all()


# ------------------------ DOCTOR CRUD ------------------------
def create_doctor(name, specialization, contact, email, password):
    

    user = User(email=email, password_hash=generate_password_hash(password), role='doctor')
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(user_id=user.id, name=name, specialization=specialization, contact=contact)
    db.session.add(doctor)
    db.session.commit()

    return doctor

def get_doctor(doctor_id):
    return Doctor.query.get(doctor_id)

def update_doctor(doctor_id, **kwargs):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return None
    for key, value in kwargs.items():
        if hasattr(doctor, key):
            setattr(doctor, key, value)
    db.session.commit()
    return doctor

def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return False
    db.session.delete(doctor)
    db.session.commit()
    return True

def search_doctors(query):
    """
    Search doctors by name, specialization, or email.
    """
    return Doctor.query.join(User).filter(
        (Doctor.name.ilike(f"%{query}%")) |
        (Doctor.specialization.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    ).all()


# ------------------------ DEPARTMENT CRUD ------------------------#

def create_department(name, description):
    department = Department(name=name, description=description)
    db.session.add(department)
    db.session.commit()
    return department

def get_department(dept_id):
    return Department.query.get(dept_id)

def update_department(dept_id, **kwargs):
    department = Department.query.get(dept_id)
    if not department:
        return None
    for key, value in kwargs.items():
        if hasattr(department, key):
            setattr(department, key, value)
    db.session.commit()
    return department

def delete_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return False
    db.session.delete(department)
    db.session.commit()
    return True

def search_departments(query):
    return Department.query.filter(Department.name.ilike(f"%{query}%")).all()
