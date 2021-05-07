from flask import redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin

from App.models import ( User, db )

def create_user(first_name, last_name, username, email, password):
    # newuser = use()
    newuser = User(first_name=first_name, last_name=last_name, username=username, email=email)
    newuser.set_password(password)
    db.session.add(newuser)
    db.session.commit()
    return True

def get_users_json():
    users = User.query.all()
    if not users:
        return jsonify([])
    json = [user.toDict() for user in users]
    return json
def get_users():
    return User.query.all()