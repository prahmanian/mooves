# Mooves API Backend

## About
Mooves is a fitness product designed to help everyday people become more active throughout their days.
Mooves consists of a series of physical card decks with specific fitness programming. For example, the 
bodyweight deck would have cards that consist of exercises that utilize the person's body weight rather
than any fitness equipment. Each card is self contained, provides the exercise, instructions and goals.
A user can thus draw and use a single card, or several for a longer workout.

The purpose of this app is to deliver this same experience digitally.

## App Deployment
This app is deployed on Heroku at the following URL:
- https://mooves.herokuapp.com/

Please note, there is currently no frontend for this app. It can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.

## Getting Started Locally

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment (venv)
We recommend working within a virtual environment whenever using Python for
projects. This keeps your dependencies for each project separate and organaized.
Instructions for setting up a virual enviornment for your platform can be found
in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python -m venv <_name_>
<_name_>/bin/activate
```

#### PIP Dependencies

Once you have your venv setup and running, install dependencies by navigating
to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages included in the requirements.txt file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://mooves.herokuapp.com

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since there is currently no frontend for the application.

## THIRD-PARTY AUTHENTICATION
#### app.py 
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'user' and 'seller' roles.

## Roles and Permissions
Registered User Roles
1) Superuser - full access to all endpoints. Must be assigned manually.
- get:decks
- get:exercises
- get:categories
- delete:decks
- delete:exercise
- delete:category
- post:exercise
- patch:exercise


2) Athlete - read only access to all GET endpoints.
- get:decks
- get:exercises
- get:categories

Public Permissions
1) GET:Decks


# Models and Endpoints
## Decks
- GET '/decks'
- DELETE '/decks/<int:deck_id>'
- POST '/decks'
- PATCH 'decks/<int:deck_id>'

## Exercises
- GET '/exercises'
- DELETE '/decexercisesks/<int:exercise_id>'
- POST '/decexercisesks'
- PATCH 'decexercisesks/<int:exercise_id>'

## Categories
- GET '/categories'
- DELETE '/categories/<int:category_id>'
- POST '/categories'
- PATCH 'categories/<int:category_id>'
