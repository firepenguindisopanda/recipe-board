from flask import Blueprint, redirect, render_template, request, jsonify, send_from_directory, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
import json
from sqlalchemy.exc import IntegrityError

user_views = Blueprint('user_views', __name__, template_folder='../templates')


from App.models import User, db
from App.controllers import ( get_users, get_users_json, create_user )
from .form import SignUp, LogIn 


@user_views.route('/', methods=['GET'])
def index():
    form = LogIn()
    return render_template('login.html', form=form)

@user_views.route('/recipes', methods=['GET'])
@login_required
def view_recipes():
    return render_template('index.html')


@user_views.route("/login", methods=['GET', 'POST'])
def loginAction():
    if request.method == 'GET':
        form = LogIn()
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        form = LogIn()
        if form.validate_on_submit():
            data = request.form
            user = User.query.filter_by(username = data['username']).first()
            if user and user.check_password(data['password']):
                flash('Login Successful!')
                login_user(user)
                return redirect(url_for('user_views.view_recipes'))
        flash('Invalid credentials')
        return redirect(url_for('user_views.index'))

         
@user_views.route("/signup", methods=['GET', 'POST'])
def signup():
    
    if request.method == "GET":
        form = SignUp() # create form object
        return render_template('signup.html', form=form) # pass form object to template
    elif request.method == "POST":
        form = SignUp()
        if form.validate_on_submit():
            userdata = request.form
            #print(userdata['first_name'])
            try:
                create_user(userdata['first_name'], userdata['last_name'], userdata['username'], userdata['email'], userdata['password'])
                
            except IntegrityError:
                db.session.rollback
                return 'Username or email already exists'
            return redirect(url_for('user_views.index'))



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