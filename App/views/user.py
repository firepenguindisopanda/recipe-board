from flask import Blueprint, redirect, render_template, request, jsonify, send_from_directory

user_views = Blueprint('user_views', __name__, template_folder='../templates')

from App.models import User
from App.controllers import ( get_users, get_users_json, create_user )
from .form import SignUp, LogIn 
#from App.controllers import ( create_user )

@user_views.route('/', methods=['GET'])
def index():
    form = SignUp() # create form object
    return render_template('signup.html', form=form) # pass form object to template

@user_views.route("/login")
def login():
    form = LogIn()
    return render_template('login.html', form=form)

@user_views.route("/signup")
def signup():
    form = SignUp() # create form object
    return render_template('signup.html', form=form) # pass form object to template

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = User.query.all()
    if not users:
        return jsonify([])
    users = [user.toDict() for user in users]
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')


@user_views.route('/api/users', methods=['POST'])
def create_user_action():
    data = request.json
    create_user(data['first_name'], data['last_name'])
    return 'Created' 