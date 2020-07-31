import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Decks, Exercises, Categories

# ATHLETE_TKN = os.environ['ATHLETE_TKN'] 
# SUPERUSER_TKN = os.environ['SUPERUSER_TKN']  

ATHLETE_TKN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Img5eFZXTDJ2aWFLNFF1UVh3TmhVMiJ9.eyJpc3MiOiJodHRwczovL21vb3Zlcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMzc3ZTgzMmNlYTMwMjIxMTQxNjBmIiwiYXVkIjoiaHR0cHM6Ly9tb292ZXMudXMvYXBpIiwiaWF0IjoxNTk2MjE1ODA3LCJleHAiOjE1OTYzMDIyMDcsImF6cCI6IlRRalJXNVVZaFBYVEI3WU0xWWtaalJoWWJ0T3J1T2hqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkZWNrcyIsImdldDpleGVyY2lzZXMiXX0.21DygWps4r1Nl8eJdVzApJrJlN0G7ruoYTHXxsU9rAa_pEkcTKjCGR3rQW4ikgEgfh-ZHB257PLpzVoWXSp2paoyWkMhYjtVXz7XlwiDsDqf9IAAnXtuxk5JEpIgSNxPlkKdmr3xpB8LV1A2T1-njxqzuUw2Gw1Bx9VFeCC6qWk-mSP1GGP0-w0EyJ9CD3l1z6kzvKUzqwBmjFZU0T7ALDOU-NaXcDsqFy2f8GRuEMc_sTqw3Nx62l1oAyXInjq5pawhLvLqb7VY5T4FsevkUK56z6QLPq6c6jE3wBeTvsu5NMKY8gkgp4EhuX1AochMBcBSXx2UwNPFPPUTEEqvNQ'
SUPERUSER_TKN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Img5eFZXTDJ2aWFLNFF1UVh3TmhVMiJ9.eyJpc3MiOiJodHRwczovL21vb3Zlcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMDgyZGNkOTNjMTAwMDNkY2IxOTc1IiwiYXVkIjoiaHR0cHM6Ly9tb292ZXMudXMvYXBpIiwiaWF0IjoxNTk2MTc1MTM5LCJleHAiOjE1OTYxODIzMzksImF6cCI6IlRRalJXNVVZaFBYVEI3WU0xWWtaalJoWWJ0T3J1T2hqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcnkiLCJkZWxldGU6ZGVja3MiLCJkZWxldGU6ZXhlcmNpc2UiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkZWNrcyIsImdldDpleGVyY2lzZXMiLCJwYXRjaDpleGVyY2lzZSIsInBvc3Q6ZXhlcmNpc2UiXX0.ob0v7ex6b5ESc_AghyYK3XSevY7BcJ_YwANvaumDUwpABC1Q7dw-ZYyb-ks9Icg5ttLze8gzYWXrDlB0K5Dm53_usjj59FoeBE_X0ZFAjllmuVQHgVlpvd1VtBtTd6RrjOCxZACETCGNTAqLDpFMvKWA32Nf2rAADocXeN1xQrA8LvhzKVwJNA15vwRShlzZ_98ck23FYGR6sJxcsddXv7iKF9NO6l9iaGMxmq0BBcvJVwFrvQiXhyvfAzeUEirYfzRxQ4dwkak_1ELvFNtZ07Y810cCSbf09apgtDOcLAajfR-0AJ3JFJxksPZcK3EERUZWlCPRSxVyocvEzpV_GA'
SUPERUSER_TKN2='eyJpc3MiOiJodHRwczovL21vb3Zlcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMDgyZGNkOTNjMTAwMDNkY2IxOTc1IiwiYXVkIjoiaHR0cHM6Ly9tb292ZXMudXMvYXBpIiwiaWF0IjoxNTk2MTc1MTM5LCJleHAiOjE1OTYxODIzMzksImF6cCI6IlRRalJXNVVZaFBYVEI3WU0xWWtaalJoWWJ0T3J1T2hqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcnkiLCJkZWxldGU6ZGVja3MiLCJkZWxldGU6ZXhlcmNpc2UiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkZWNrcyIsImdldDpleGVyY2lzZXMiLCJwYXRjaDpleGVyY2lzZSIsInBvc3Q6ZXhlcmNpc2UiXX0'
SUPERUSER_TKN3='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Img5eFZXTDJ2aWFLNFF1UVh3TmhVMiJ9.eyJpc3MiOiJodHRwczovL21vb3Zlcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMDgyZGNkOTNjMTAwMDNkY2IxOTc1IiwiYXVkIjoiaHR0cHM6Ly9tb292ZXMudXMvYXBpIiwiaWF0IjoxNTk2MjA5OTc1LCJleHAiOjE1OTYyOTYzNzUsImF6cCI6IlRRalJXNVVZaFBYVEI3WU0xWWtaalJoWWJ0T3J1T2hqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcnkiLCJkZWxldGU6ZGVja3MiLCJkZWxldGU6ZXhlcmNpc2UiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkZWNrcyIsImdldDpleGVyY2lzZXMiLCJwYXRjaDpleGVyY2lzZSIsInBvc3Q6ZXhlcmNpc2UiXX0.nXoAUOCwYxi5u6YDHkCT6rnyduMSNHWqEIFYjrtjnORZu3Awd_2T_uUlni0bXVBTvVtlY1SC5H9CMAQwHJcuqWhWO3m6jbfai6zssaD_61FBr47n66Gg9ROIg9qjf4-ZqPMy1GZUbBZ0oAkv6UWFbovuRH06Bb16RMcVl3NhJ_vOs70iJVV3gHAres17bs1kKWWn75ItVjoXQyCsHoPqD-i-IlTJ53hW-9qr83PXbdxfl4SV0hjLyKyCDRV3rPl4FWWKNCogh-USf-diMLv1Ho1u93Bgn1YQihRZbDiMXaSaNOjV9pXZeEj4v5OJWLz7jvcoEmfJzjMhtg1WjLbrjw'

class MoovesTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "mooves_test"  # TODO update
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
        self.assertGreaterEqual(len(data['decks']), 0)

    def test_get_decks_with_variable(self):
        res = self.client().get('/decks/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

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

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], "Not found")

    def test_athlete_get_exercises(self):
        res = self.client().get(
            '/exercises', headers={'Authorization': 'Bearer ' + str(SUPERUSER_TKN3)})
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

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

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

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

if __name__ == "__main__":
    unittest.main()