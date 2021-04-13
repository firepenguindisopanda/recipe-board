from flask import redirect, render_template, request, session, url_for

from App.models import ( User )

'''
def create_user(firstname, lastname, uwi_id, email, gender, dob):
    # newuser = use()
    newuser = User(firstname=firstname, lastname=lastname)
    db.session.add(newuser)
    db.session.commit()
'''
def create_user(firstname, lastname):
    # newuser = use()
    newuser = User(first_name=firstname, last_name=lastname)
    db.session.add(newuser)
    db.session.commit()

def get_users_json():
    users = User.query.all()
    if not users:
        return jsonify([])
    json = [user.toDict() for user in users]
    return json
def get_users():
    return User.query.all()