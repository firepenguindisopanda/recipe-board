from flask import redirect, render_template, request, session, url_for

from App.models import ( User, db )

'''
def create_user(firstname, lastname, uwi_id, email, gender, dob):
    # newuser = use()
    newuser = User(firstname=firstname, lastname=lastname)
    db.session.add(newuser)
    db.session.commit()
'''
def create_user(first_name, last_name):
    # newuser = use()
    newuser = User(first_name=first_name, last_name=last_name)
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