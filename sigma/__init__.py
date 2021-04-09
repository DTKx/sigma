import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY']='4ebebae9544f86c19558bc018c7ea517'# Secret Key protect form modified cookies,forgery attacks etc
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'# Location of our sqllite, /// represents a relative path this means that our file should be created in the module we are currently in right now.
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')

from sigma import routes
