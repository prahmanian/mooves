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

#### Export Configuration Variables

Once you've installed the dependencies, you should export the local configuration variables located in the setup.sh file.

```bash
source setup.sh
```

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
The JWT token contains the permissions for the 'athlete' and 'superuser' roles.

## Roles and Permissions
Registered User Roles
### Superuser - full access to all endpoints. Must be assigned manually.
- get:decks
- get:exercises
- get:categories
- delete:decks
- delete:exercise
- delete:category
- post:exercise
- patch:exercise

#### Getting Fresh Superuser Token
1. Go to https://mooves.herokuapp.com (https://mooves.us.auth0.com/authorize?audience=https://mooves.us/api&response_type=token&client_id=TQjRW5UYhPXTB7YM1YkZjRhYbtOruOhj&redirect_uri=http://127.0.0.1:5000/callback)
2. Click on Login and enter the following credentials into Auth0, which has been designated with Superuser role:
   Email: pedram+moovesadmin@gutenmade.com
   Password: M00v3$2020

#### Sample Superuser JWT

### Athlete - read only access to all GET endpoints.
- get:decks
- get:exercises
- get:categories

#### Getting Fresh Athlete Token
1. Go to https://mooves.herokuapp.com (https://mooves.us.auth0.com/authorize?audience=https://mooves.us/api&response_type=token&client_id=TQjRW5UYhPXTB7YM1YkZjRhYbtOruOhj&redirect_uri=http://127.0.0.1:5000/callback)
2. Click on Login and enter the following credentials into Auth0, which has been designated with Superuser role:
   Email: pedram+moovesathlete@gutenmade.com
   Password: M00v3$2020

#### Sample Athlete JWT

### Public Permissions
- get:decks

 
 ## Testing
Unit tests are provided in test_app.py. To run this file use:
'''
dropdb mooves_test
createdb mooves_test
python test_app.py
'''

Further, the file 'Mooves.postman_collection.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> directory/warranty-tracker-test-endpoints.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## Data Modeling
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are three tables created: Decks, Exercises, and Categories
- Decks are the collections of workout cards.
- Exercises are the building blocks of the workout cards.
- Categories help organize the workout cards based on the muscle groups they target.
Each table inherits insert, update, delete, and format helper functions.

## Models and Endpoints

### Decks

#### GET '/decks'
Returns a list of all decks in the database, and a success value. This endpoint is accessible to authenticated users.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/decks 
Sample response output:
{
  "decks": [
    {
        'id': 1,
        'code': 'BW',
        'name': 'Bodyweight Heavyweight',
        'theme': 'Bodyweight Only',
        'description': 'Our no excuses deck!',
        'requisites': 'None'
    }
  ],
  "success": true
}

#### DELETE '/decks/<int:deck_id>'
Returns a list of all decks after deleting the requested deck, a success value, and the id of the deleted deck.
This endpoint is accessible to users with the Superuser role permissions.
Sample curl:
curl http://localhost:5000/decks/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "decks": [],
  "success": true,
  "deleted": 1
}

- Future Endpoints
#### POST '/decks'
#### PATCH '/decks/<int:deck_id>'

### Exercises

#### GET '/exercises'
Returns a list of all exercises in the database, and a success value. This endpoint is accessible to authenticated users.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/exercises 
Sample response output:
{
  "exercises": [
    {
        'id': 1,
        'name': 'Slow Down Pushups',
        'prompt': 'In normal pushup formation, lower yourself slowly, counting to 5, then explosively push up.',
        'level': 2
    },
    {
        'id': 2,
        'name': 'Good Mornings',
        'prompt': 'Stand upright with feet shoulderwidth apart, hinge at the hips down near a 90 degree angle.',
        'level': 1
    }
  ],
  "success": true
}

#### GET '/exercises/<int:exercise_id>'
Returns an object with the requested exercise object and a success value. This endpoint is accessible to authenticated users.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/exercises/1 
Sample response output:
{
  "exercise": {
        'id': 1,
        'name': 'Slow Down Pushups',
        'prompt': 'In normal pushup formation, lower yourself slowly, counting to 5, then explosively push up.',
        'level': 2
    },
  "success": true
}

#### DELETE '/exercises/<int:exercise_id>'
Returns a list of all exercises after deleting the requested exercise, a success value, and the id of the deleted exercise.
This endpoint is accessible to users with the Superuser role permissions.
Sample curl:
curl http://localhost:5000/exercises/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "exercises": [],
  "success": true,
  "deleted": 1
}

#### POST '/exercises'
Returns a success value after creating and posting a new exercise.
This endpoint is accessible to users with the Superuser role permissions.
Sample curl: 
curl http://localhost:5000/exercises -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Slow Down Pushups", "level": 2, "prompt": "In normal pushup formation, lower yourself slowly, counting to 5, then explosively push up."}'

Sample response output:
{
  "success": true,
}

#### PATCH 'exercises/<int:exercise_id>'
Returns a success value after updating the requested exercise.
This endpoint is accessible to users with the Superuser role permissions.
Sample curl: 
curl http://localhost:5000/exercises/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"level": 5}'

Sample response output:
{
  "success": true,
}

### Categories

#### GET '/categories'
Returns a list of all categories in the database, and a success value. This endpoint is accessible to authenticated users.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/categories 
Sample response output:
{
  "categories": [
    {
        'id': 1,
        'name': 'Back',
        'color': '#ff0000',
    }
  ],
  "success": true
}

#### DELETE '/categories/<int:category_id>'
Returns a list of all categories after deleting the requested category, a success value, and the id of the deleted category.
This endpoint is accessible to users with the Superuser role permissions.
Sample curl:
curl http://localhost:5000/categories/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "categories": [],
  "success": true,
  "deleted": 1
}

- Future Endpoints
#### POST '/categories'
#### PATCH '/categories/<int:category_id>'