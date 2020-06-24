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
    movies = db.relationship('Movies', backref='auther', lazy=True)

    def __repr__(self):
        return f"user('{self.name}', '{self.email}', '{self.profile_pic}')"

# Post model
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    movie_country = db.Column(db.String(100), nullable=False)
    movie_duration = db.Column(db.String(100), nullable=False)
    movie_genre = db.Column(db.String(100), nullable=False)
    movie_date_added = db.Column(db.String(100), nullable=False)
    movie_title = db.Column(db.String(100), nullable=False)
    movie_description = db.Column(db.String(100), nullable=False)
    movie_image = db.Column(db.String(20), unique=False, nullable=False, default='https://live.staticflickr.com/4422/36193190861_93b15edb32_z.jpg')
    #ForeignKey has relationship with user model
    # user.id refrences table name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.movie_title}', '{self.date_posted}', '{self.movie_country}', '{self.movie_image}', '{self.movie_description}', '{self.movie_genre}', '{self.movie_date_posted}'"

"""class Movies (db.Model):
    id = db.Column(db.String(100), primary_key=True)
    person_id = db.Column(db.String(100), db.ForeignKey('user.id', nullable=False))
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    def __repr__(self):
        return f"Movies('{image_file}')"
"""
    

"""class FacebookUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique =True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    profile_pic = db.Column(db.String(100), unique=False, nullable=True)
"""