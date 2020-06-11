from InstaFlix import db, login_manager
from datetime import timedelta, datetime
from flask_login import UserMixin

REMEMBER_COOKIE_DURATION = timedelta(seconds=1)

# Figure out how to allow log in for Facebook, Google and regular
# Get a user by their ID

@login_manager.user_loader
def load_user(user_id, duration=REMEMBER_COOKIE_DURATION):
    print("Here is the user_id: ",user_id)
    #print(type(user_id))
    return User.query.get(user_id)
    
"""class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique =True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.String(100), unique=False, nullable=False, default='default.jpg')
"""
class User(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique =True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    profile_pic = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return f"user('{self.name}', '{self.email}', '{self.profile_pic}')"
    

"""class FacebookUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique =True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    profile_pic = db.Column(db.String(100), unique=False, nullable=True)
"""