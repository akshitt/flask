from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
#!--------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fe8a028d74aa4501203b3cc679d7e424'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#!--------------------------------------------------------------------------------------

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#!--------------------------------------------------------------------------------------

from flaskblog import routes 
