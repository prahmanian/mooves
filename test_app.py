import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Decks, Exercises, Categories


class MoovesTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"  # TODO update
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)  # TODO update
        setup_db(self.app, self.database_path)

        self.new_deck = {
            'code': 'BW',
            'name': 'Bodyweight Heavyweight',
            'theme': 'Bodyweight Only',
            'description': 'Our no excuses deck!',
            'requisites': 'None'
        }

        self.patch_deck = {
            'code': 'BW',
            'name': 'Bodyweight Heavyweight',
            'theme': 'Bodyweight Only',
            'description': 'Our no excuses deck!',
            'requisites': 'None'
        }

        self.new_exercise = {
            'name': 'Slow Down Pushups',
            'prompt': 'In normal pushup formation, lower yourself slowly,' +
                      ' counting to 5, then explosively push up. ',
            'level': 2,
        }

        self.patch_exercise = {
            'level': 1,
        }

        self.new_category = {
            'name': 'Back',
            'color': '#ff0000',

        }

        self.patch_category = {
            'name': 'Back',
            'color': '#ffff00',

        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # #------ POST ENDPOINTS ------#
    # #------ -------------- ------#

    # #------ Tests for POST /exercises ------#

    def test_add_exercise(self):
        res = self.client().post('/exercises', json=self.new_exercise)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_exercise_creation(self):
        res = self.client().post('/exercises/45', json=self.new_exercise)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # #------ GET ENDPOINTS ------#
    # #------ ------------- ------#

    # #------ Tests for GET /decks ------#
    def test_get_decks(self):

        res = self.client().get('/decks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['decks']))

    def test_get_decks_with_variable(self):
        res = self.client().get('/decks/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    # #------ Tests for GET /exercises ------#
    def test_get_exercises(self):
        res = self.client().get('/exercises')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['exercises']))

    # TODO test for exiting exercise by id

    def test_get_exercises_with_variable(self):
        res = self.client().get('/exercises/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    # #------ Tests for GET /categories ------#
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_categories_with_variable(self):
        res = self.client().get('/categories/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    # #------ PATCH ENDPOINTS ------#
    # #------ --------------- ------#

    # #------ Tests for PATCH /exercises/<int:exercise_id> ------#

    def test_add_exercise(self):

        res = self.client().patch('/exercises/1', json=self.patch_exercise)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_exercise_creation(self):
        res = self.client().patch('/exercises/45', json=self.patch_exercise)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # #------ DELETE ENDPOINTS ------#
    # #------ ---------------- ------#

    # #------ Tests for DELETE /decks/<int: deck_id> ------#

    def test_delete_decks(self):

        res = self.client().delete('/decks/4')
        data = json.loads(res.data)

        deck = Decks.query.filter(Decks.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('deleted')
        self.assertTrue('decks')
        self.assertEqual(deck, None)

    def test_delete_deck_not_found(self):
        res = self.client().delete('/decks/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_delete_decks_not_allowed(self):
        res = self.client().delete('/decks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")

    # #------ Tests for DELETE /exercises/<int: exercise_id> ------#

    def test_delete_exercises(self):
        res = self.client().delete('/exercises/4')
        data = json.loads(res.data)

        exercise = Exercises.query.filter(Exercises.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('deleted')
        self.assertTrue('exercises')
        self.assertEqual(exercise, None)

    def test_delete_exercises_not_found(self):
        res = self.client().delete('/exercises/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_delete_exercises_not_allowed(self):
        res = self.client().delete('/exercises')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")

    # #------ Tests for DELETE /categories/<int: category_id> ------#

    def test_delete_categories(self):
        res = self.client().delete('/categories/4')
        data = json.loads(res.data)

        category = Categories.query.filter(Categories.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('deleted')
        self.assertTrue('categories')
        self.assertEqual(category, None)

    def test_delete_categories_not_found(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_delete_categories_not_allowed(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")
