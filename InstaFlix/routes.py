from InstaFlix import application, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, Flask, session
from oauthlib.oauth2 import WebApplicationClient
from os import environ
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from tmdbv3api import TMDb
from tmdbv3api import Movie

# Import data from models.py file
from InstaFlix.models import User, Movies

import requests
import json
import csv
import random

# API Key
api_key = environ.get("api_key")

# The Movie DB Key
tmdb = TMDb()
tmdb.api_key = environ.get("the_movie_db_key")
tmdb.language = 'en'
tmdb.debug = True
the_movie_db_key = environ.get("the_movie_db_key")

# Facebook Configuration
FB_CLIENT_ID =  environ.get("FB_CLIENT_ID")
FB_CLIENT_SECRET = environ.get("FB_CLIENT_SECRET")

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

# GOOGLE Configuration
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration")


print(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
# User session management setup
# https://flask-login.readthedocs.io/en/latest


# 0Auth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Flask-Login helper to retrieve a user from our db


@application.route('/password')
def something():
    return f

@application.route("/")
def index():
    #print(current_user)
    if current_user.is_authenticated:
        return dashboard()
        """" (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            ) 
        ) """
    else:
        return render_template("home.html")
        #return '<a class="button" href="/login">Google Login</a>'

# Provide error handling in case GOOGLE API returns a failure in the future


@application.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

URL = "https://127.0.0.1:5000"
FB_SCOPE = ["email"]
@application.route("/login/fb")
def login_facebook():
    # Do something
    facebook = OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)
    return redirect(authorization_url)

@application.route("/fb-callback")
def fb_callback():
    facebook = OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=request.url,
    )

    # Fetch a protected resource, ex user profile, via Graph API

    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    users_email = facebook_user_data["email"]
    users_name = facebook_user_data["name"]
    picture = facebook_user_data.get("picture", {}).get("data", {}).get("url")
    unique_id = facebook_user_data["id"]

    # Create a user in your db with the information provided
    # by Facebook
    user = User.query.filter_by(email=users_email).first()
    print("This is your user: ", user)
    if user:
        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("index"))

    # Create a user in your db with the information provided
    # by Google
    new_user = User(id=unique_id, email=users_email, name=users_name, profile_pic=picture)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    

    # Begin user session by logging the user in
    login_user(new_user)

    # Send user back to homepage
    return redirect(url_for("index"))

@application.route("/login/callback")
def callback():
    # Get authroization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authroized your
    # app, and now you've verified their email through Google!

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User.query.filter_by(email=users_email).first()
    print(user)
    if user:
        # Begin user session by logging the user in
        print(user)
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("index"))

    # Create a user in your db with the information provided
    # by Google
    new_user = User(id=unique_id, email=users_email, name=users_name, profile_pic=picture)

    # add the new user to the database
    # print(new_user)
    db.session.add(new_user)
    db.session.commit()

    # Begin user session by logging the user in
    #print(new_user)
    login_user(new_user)

    # Send user back to homepage
    return redirect(url_for("index"))

@application.route('/signup')
def signup_post():
    index()
    return render_template("signup.html")

@application.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))


@application.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    movies = None
    profile_pic = current_user.profile_pic
    name = current_user.name
    print(profile_pic)
    # randomly select a movie
    with open('catalog.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))

    kaggle_movie = {
        'id': row[0],
        'category': row[1],
        'title': row[2],
        'director': row[3],
        'cast': row[4],
        'country': row[5],
        'date_added': row[6],
        'release_year': row[7],
        'maturity': row[8],
        'duration': row[9],
        'genre': row[10],
        'description': row[11],
        # default poster just so we see something
        'image': 'https://live.staticflickr.com/4422/36193190861_93b15edb32_z.jpg',
        'imdb': 'Not Available'
   }

    # fetch cover image
    # call OMDB database
    omdb_url = f"http://www.omdbapi.com/?t={kaggle_movie['title']}/&apikey={api_key}"
    # get back the response
    omdb_response = requests.request("GET", omdb_url)
    # parse result into JSON and look for matching data if available

    the_movie_db_url = f"https://api.themoviedb.org/3/search/movie?api_key={the_movie_db_key}&query={kaggle_movie['title']}"
    the_movie_db_response = requests.request("GET", the_movie_db_url)

    the_movie_db_data = the_movie_db_response.json()
    #print(the_movie_db_data)
    '''if 'total_pages' in the_movie_db_data:
        kaggle_movie['the_movie_db_total_pages'] = the_movie_db_data['total_pages']
        #print("SUCCESSFUL ", kaggle_movie['the_movie_db_total_pages'])  
    '''

    if 'results' in the_movie_db_data:
        try:
            kaggle_movie['the_movie_db_results'] = the_movie_db_data["results"][0]["id"]
            print("Results SUCCESSFUL ", kaggle_movie['the_movie_db_results'])
        except IndexError:
            kaggle_movie['the_movie_db_results'] = 'null'

    omdb_movie_data = omdb_response.json()
    if 'Poster' in omdb_movie_data:
        kaggle_movie['image'] = omdb_movie_data['Poster']
    if 'imdbRating' in omdb_movie_data:
        kaggle_movie['imdb'] = omdb_movie_data['imdbRating']
    
    the_movie_db_video_query_url = f"https://api.themoviedb.org/3/movie/{kaggle_movie['the_movie_db_results']}/videos?api_key={the_movie_db_key}"
    print(the_movie_db_video_query_url)
    the_movie_db_video_response = requests.request("GET", the_movie_db_video_query_url)
    
    the_movie_db_video_data = the_movie_db_video_response.json()
    #print(the_movie_db_video_data)

    if "results" in the_movie_db_video_data:
        try:
            kaggle_movie['the_movie_db_video'] = the_movie_db_video_data["results"][0]["key"]
            print("Key SUCCESSFUL", kaggle_movie['the_movie_db_video'])
        except:
            kaggle_movie['the_movie_db_video'] = 'null'
    elif "results" in the_movie_db_video_data  < 0:
        #kaggle_movie['the_movie_db_video'] = 'null'
        print("Results are False")
    elif "results" not in the_movie_db_video_data:
        #kaggle_movie['the_movie_db_video'] = 'null'
        print("Results not available")
    #print(the_movie_db_video_data, "TEST SUCCESSFUL")


    '''
    user_favorites = current_user
    print(movie['title'])

    if request.form:
        try:
            Grab the "movie" input from the form and use it to initilaize
                a new movie object. We save this new Movie to a variable named 
                movie.
            
            user_movie = Movies(movie_title=request.form.get())
    '''



    
    return render_template("dashboard.html", movie=kaggle_movie, profile_pic = current_user.profile_pic, name = current_user.name)

@application.route("/account")
def application():
    profile_pic = current_user.profile_pic
    name = current_user.name
    email = current_user.email
    return render_template("account.html", profile_pic = current_user.profile_pic, name = current_user.name, email=email)