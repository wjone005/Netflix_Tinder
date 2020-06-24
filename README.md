# InstaFlix - 'Tinder/Instagram' for Netflix 🍿

A Flask app that generates random movie recommendations, with details listed for each title, that a user can swipe through and watch with the click of a button.

![app demo](/InstaFlix/static/images/website.gif)

## Installation
1. Install Requirements 

    ```$ pip3 install -r requirements.txt (Python 3)```

2. Obtain an API Key for OMDB, Google, and Facebook. Set the keys as an environment variable
    Using the following format for macOS and Linux Distributions:

    ```
    export KEY=value
    export GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID
    export GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET
    export FB_CLIENT_ID=FB_CLIENT_ID
    export FB_CLIENT_SECRETD=FB_CLIENT_SECRET
    export api_key=api_key
    
    ```

    and add them with the following format `KEY = environ.get("value")`

    If you are ever adding your own code to GitHub and choose to use a `.env` file, make sure it's listed under a `.gitignore` file. Therefore, it doesn't accidently get published to GitHub!=

3. Download the CSV linked in [this Kaggle dataset](https://www.kaggle.com/shivamb/netflix-shows) and name the file `catalog.csv`. This will store the bulk of our data.

## Usage
#### To launch the app:
    $ python application.py or python3 application.py

Once the Flask app is running, navigate to the `localhost` link provided:

<code> * Running on <b>https://127.0.0.1:5000/</b> (Press CTRL+C to quit)</code>


## Special Thanks

* [Harshi Starter Code](https://github.com/harshibar) - She originally came up with the idea, I added more features.
* [Open Movie Database](http://www.omdbapi.com/) - Movie data API to fetch movie poster links and IMDB scores
* [Kaggle Netflix Dataset](https://www.kaggle.com/shivamb/netflix-shows) - Comprehensive dataset with many Netflix movies/tv shows and their metadata
* [Facebook API](https://developers.facebook.com/docs/apps/) - Documentation on how to setup Facebook Login API
* [Google API](https://developers.google.com/identity) - Documentation on how to setup Google Login API


## Learn More

* [Flask Starter Guide](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/) - A great starter guide on how to learn Flask
* [Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - A more in-depth tutorial on Flask
* [About .gitignore and config files](https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c) - A step-by-step guide on how to hide your API keys

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com\InstaFlix\LICENSE) file for details.

## Agile Board
* [InstaFlix Trello Agile Board](https://trello.com/b/SEMkB36D/instaflix-project)

## Features Added
* Google Authentication
* Facebook Authentication
* Database to keep track of users
* Social profile icon on dashboard

## Future Features Currently Working On
* Watch trailers
* Allow adding friends 
* Show movies your friends both liked. To watch together.
* Filter movies by category
* Add liked moves to be saved to database for future reference
* Allow updating of profile picture
* Dockerize this project