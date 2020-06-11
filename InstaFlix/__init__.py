# Python standard libraries
import os
from flask import Flask

# Import SQL
from flask_sqlalchemy import SQLAlchemy

# Import Bcrypt to encrypt passwords
from flask_bcrypt import Bcrypt

# Third-party libraries
from flask_login import LoginManager

application = Flask(__name__)
application.secret_key = os.urandom(24)

# Location where database will be and created
# /// means relative path from current file
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# SQLAlchemy instance
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)

login_manager.init_app(application)

# Place here to prevent circular import error
from InstaFlix import routes