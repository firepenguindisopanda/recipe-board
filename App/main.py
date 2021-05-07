import os
from flask import Flask
from flask_jwt import JWT
from datetime import timedelta 
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin

from App.models import db, User

from App.views import (
    api_views,
    user_views
)

''' Begin boilerplate code '''
''' Begin Flask Login Functions '''
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


''' End Flask Login Functions '''

def get_db_uri(scheme='sqlite://', user='', password='', host='//demo.db', port='', name=''):
    return scheme+'://'+user+':'+password+'@'+host+':'+port+'/'+name 

def loadConfig(app):
    #try to load config from file, if fails then try to load from environment
    try:
        app.config.from_object('App.config')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if app.config['SQLITEDB'] else app.config['DBURI']
    except:
        print("config file not present using environment variables")
        # DBUSER = os.environ.get("DBUSER")
        # DBPASSWORD = os.environ.get("DBPASSWORD")
        # DBHOST = os.environ.get("DBHOST")
        # DBPORT = os.environ.get("DBPORT")
        # DBNAME = os.environ.get("DBNAME")
        DBURI = os.environ.get("DBURI")
        SQLITEDB = os.environ.get("SQLITEDB", default="true")
        app.config['ENV'] = os.environ.get("ENV")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if SQLITEDB in {'True', 'true', 'TRUE'} else DBURI

def create_app():
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    login_manager.init_app(app)
    db.init_app(app)
    return app

app = create_app()

app.app_context().push()

app.register_blueprint(api_views)
app.register_blueprint(user_views)

''' Set up JWT here (if using flask JWT)'''
def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''