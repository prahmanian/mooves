import os
from flask import Flask, request, abort, jsonify, json, redirect, render_template, session, url_for, _request_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Decks, Exercises, Categories
# from auth import *
# Auth0 imports below
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen
import constants
from jose import jwt


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.secret_key = constants.SECRET_KEY
  app.debug = True
  setup_db(app)
  CORS(app, resources={r"/*": {"origins":"*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  # _________________________________________
  # Add Third Party Auth with Auth0
  # _________________________________________
  ENV_FILE = find_dotenv()
  if ENV_FILE:
    load_dotenv(ENV_FILE)

  # AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
  # AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
  # AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
  # AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
  # AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
  # AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

  AUTH0_CALLBACK_URL = env['AUTH0_CALLBACK_URL']
  AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
  AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
  AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
  AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
  AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
  API_AUDIENCE = env.get('API_AUDIENCE')
  ALGORITHMS = ['RS256']

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
  
  # AuthError Exception - A standardized way to communicate auth failure modes
  class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

  # Format error response and append status code
  def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token
  
  #Determines if the Access Token is valid
  def requires_auth(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated
  
  # Determines if the required scope is present in the Access Token
  # Args: required_scope (str): The scope required to access the resource
  def requires_scope(required_scope):
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False

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
  @requires_auth
  def get_decks():
    if requires_scope("get:decks"):
      db_decks= Decks.query.all()
      if len(db_decks) == 0:
          decks = [] 
      else:
          decks = [deck.format() for deck in db_decks]
      return jsonify({
          "success": True,
          "decks": decks
      })
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

  @app.route('/exercises', methods=['GET'])
  @requires_auth
  def get_exercises():
    if requires_scope("get:exercises"):
      db_exercises= Exercises.query.all()
      if len(db_exercises) == 0:
          exercises = [] 
      else:
          exercises = [exercise.format() for exercise in db_exercises]
      return jsonify({
          "success": True,
          "exercises": exercises
      })
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

  @app.route('/exercises/<int:exercise_id>', methods=['GET'])
  @requires_auth
  def get_exercises(exercise_id):
    if requires_scope("get:exercises"):
          exercise= Exercises.query.filter(Exercises.id == exercise_id).one_or_none()
          if exercise is None:
                abort(404)
          exercise = exercise.format()
          return jsonify({
          "success": True,
          "exercise": exercise
          })
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

  @app.route('/categories', methods=['GET'])
  @requires_auth
  def get_categories():
    if requires_scope("get:categories"):
      db_categories = Categories.query.all()
      if len(db_categories) == 0:
          categories = [] 
      else:
          categories = [category.format() for category in db_categories]
      return jsonify({
          "success": True,
          "categories": categories
      })
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


  # _________________________________________
  # Delete Routes
  # _________________________________________
  
  @app.route('/decks/<int:deck_id>', methods=['DELETE'])
  @requires_auth
  def delete_deck(deck_id):
    if requires_scope("delete:decks"):
      try:
        deck = Decks.query.filter(Decks.id == deck_id).one_or_none()
        if deck is None:
          abort(404)
        deck.delete()
        decks = [deck.format() for deck in Decks.query.all()]

        return jsonify({
          "success": True,
          "deleted": deck_id,
          "decks": decks
        })
      except:
        abort(422)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


  @app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
  @requires_auth
  def delete_deck(exercise_id):
    if requires_scope("delete:exercise"):
      try:
        exercise = Exercises.query.filter(Exercises.id == exercise_id).one_or_none()
        if exercise is None:
          abort(404)
        exercise.delete()
        exercises = [exercise.format() for exercise in Exercises.query.all()]

        return jsonify({
          "success": True,
          "deleted": exercise_id,
          "exercises": exercises
        })
      except:
        abort(422)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

  @app.route('/categories/<int:category_id>', methods=['DELETE'])
  @requires_auth
  def delete_deck(category_id):
    if requires_scope("delete:category"):
      try:
        category = Categories.query.filter(Categories.id == category_id).one_or_none()
        if category is None:
          abort(404)
        category.delete()
        categories = [category.format() for category in Categories.query.all()]

        return jsonify({
          "success": True,
          "deleted": category_id,
          "categories": categories
        })
      except:
        abort(422)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


  # _________________________________________
  # POST Routes
  # _________________________________________

  @app.route('/exercises', methods=['POST'])
  def add_exercise():
        data_string = request.data
        new_exercise_data = json.loads(data_string)

        name = new_exercise_data['name']
        prompt = new_exercise_data['prompt']
        level = new_exercise_data['level']


       

        try:
           new_exercise = Exercises(name, prompt, level)
           new_exercise.insert()
           return jsonify({
            'success':True
            })
        except:
          abort(422)

  # _________________________________________
  # PATCH Routes
  # _________________________________________

  @app.route('/exercises/<int:exercise_id>', methods=['PATCH'])
  def add_exercise(exercise_id):
        data_string = request.data
        update_data = json.loads(data_string)

        exercise = Exercises.query.filter(Exercises.id == exercise_id).one_or_none()

        if exercise is None:
              abort(404)

        name = update_data['name']
        prompt = update_data['prompt']
        level = update_data['level']

        if name:
              exercise.name = name
        if prompt:
              exercise.prompt = prompt
        if level:
              exercise.level = level

        try:
           exercise.update()
           return jsonify({
            'success':True
            })
        except:
          abort(422)

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

mooves_app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)