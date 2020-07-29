import os
from flask import Flask, request, abort, jsonify, json, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Decks, Exercises, Categories
from auth import *
# Auth0 imports below
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import constants


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.secret_key = constants.SECRET_KEY
  app.debug = True
  setup_db(app)
  CORS(app, resources={r"/*": {"origins":"*"}})

  # _________________________________________
  # Add Third Party Auth with Auth0
  # _________________________________________
  ENV_FILE = find_dotenv()
  if ENV_FILE:
    load_dotenv(ENV_FILE)

  AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
  AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
  AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
  AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
  AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
  AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
  
  oauth = OAuth(app)

  auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)
  
  # _________________________________________
  # Auth Controllers 
  # _________________________________________

  @app.route('/')
  def home():
        return render_template('home.html')


  # Here we're using the /callback route.
  @app.route('/callback')
  def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    # session['jwt_payload'] = userinfo
    session[constants.JWT_PAYLOAD] = userinfo
    # session['profile'] = {
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

  @app.route('/login')
  def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

  @app.route('/dashboard')
  @requires_auth
  def dashboard():
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))
  
  @app.route('/logout')
  def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

  # _________________________________________
  


  # _________________________________________
  # Read Routes
  # _________________________________________
  
  @app.route('/decks', methods=['GET'])
  @requires_auth('get:decks')
  def get_decks(token):
    db_decks= Decks.query.all()
    if len(db_decks) == 0:
        decks = [] 
    else:
        decks = [deck.format() for deck in db_decks]
    return jsonify({
        "success": True,
        "decks": decks
    })

  @app.route('/exercises', methods=['GET'])
  @requires_auth('get:exercises')
  def get_exercises(token):
    db_exercises= Exercises.query.all()
    if len(db_exercises) == 0:
        exercises = [] 
    else:
        exercises = [exercise.format() for exercise in db_exercises]
    return jsonify({
        "success": True,
        "exercises": exercises
    })

  @app.route('/categories', methods=['GET'])
  @requires_auth('get:categories')
  def get_categories(token):
    db_categories = Categories.query.all()
    if len(db_categories) == 0:
        categories = [] 
    else:
        categories = [category.format() for category in db_categories]
    return jsonify({
        "success": True,
        "categories": categories
    })

  # _________________________________________
  # Error Handlers
  # _________________________________________

  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
          "success":False,
          "error": 404,
          "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
          "success":False,
          "error": 422,
          "message": "unprocessable"
        }), 422

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
          "success":False,
          "error": 400,
          "message": "bad request"
        }), 400

  @app.errorhandler(405)
  def not_allowed(error):
        return jsonify({
          "success":False,
          "error": 405,
          "message": "method not allowed"
        }), 405
  
  @app.errorhandler(500)
  def server_error(error):
        return jsonify({
          "success":False,
          "error": 500,
          "message": "internal server error"
        }), 500


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)