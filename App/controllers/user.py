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
    newuser = User(firstname=firstname, lastname=lastname)
    db.session.add(newuser)
    db.session.commit()