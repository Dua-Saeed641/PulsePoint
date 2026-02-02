from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

def register_user(email, password, role):
    if not email or not password or not role:
        return None
    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):

    admin_email=current_app.config.get('SECRET_ADMIN_EMAIL')
    admin_password=current_app.config.get('SECRET_ADMIN_PASSWORD')

    if email ==admin_email and password== admin_password:
        admin_user=User.query.filter_by(email=admin_email, role='admin').first()

        if not admin_user:
            admin_user= User(email=admin_email, role= 'admin')
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()

        return admin_user

    #regular user auth
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
