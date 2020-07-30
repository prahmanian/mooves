# mooves
Mooves is a fitness product designed to help everyday people become more active throughout their days.
Mooves consists of a series of physical card decks with specific fitness programming. For example, the 
bodyweight deck would have cards that consist of exercises that utilize the person's body weight rather
than any fitness equipment. Each card is self contained, provides the exercise, instructions and goals.
A user can thus draw and use a single card, or several for a longer workout.

The purpose of this app is to deliver this same experience digitally.

# App Location
This app is deployed on Heroku at the following domain:
- https://mooves.herokuapp.com/


# Roles and Permissions
Registered User Roles
1) Superuser - full access to all endpoints. Must be assigned manually.
2) Athlete - read only access to all GET endpoints.

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
