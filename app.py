import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Decks, Exercises, Categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins":"*"}})

  @app.route('/')
  def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting


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