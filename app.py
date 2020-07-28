import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting



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