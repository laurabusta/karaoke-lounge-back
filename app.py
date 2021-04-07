# activate virtual environment in terminal >> . venv/bin/activate
# start app from terminal with >> python3 app.py

from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.songs import song
from resources.profile import profile

DEBUG = True
PORT = 8000

login_manager = LoginManager() # sets up ability to start the session

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" # Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_profile(profileID):
    try:
        return models.Profile.get(models.Profile.id == profileID)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(song, origins=['http://localhost:19006'], supports_credentials=True)
app.register_blueprint(song, url_prefix='/api/v1/songs')

CORS(profile, origins=['http://localhost:19006'], supports_credentials=True)
app.register_blueprint(profile, url_prefix='/profile')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)