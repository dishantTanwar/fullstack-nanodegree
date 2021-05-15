import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from config import db_setup, SQLALCHEMY_TRACK_MODIFICATIONS
# "postgresql://db_setup["user_name"]:dbsetup["password"]@{}/{}".format(db_setup["port"] db_setup["database_name_test"])

database_path = f'postgresql://{db_setup["user_name"]}:{db_setup["password"]}@{db_setup["port"]}/{db_setup["database_name_test"]}'

class TriviaTestCase(unittest.TestCase):  
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.

    """
#----------------------------------------------------------------------------#
# Test Categories
#----------------------------------------------------------------------------#

    def test_show_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_show_questions(self):
        res =  self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_show_questions_abort_400(self):
        res =  self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    ## create new question
    def test_create_question(self):
        # request header
        req = {
            'question':  'Heres a new question',
            'answer':  'Heres a new answer',
            'difficulty': 1,
            'category': 3,
        }

        res = self.client().post('/questions', json = req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_create_question_error_400(self):
        # request header
        req = {}

        res = self.client().post('/questions', json = req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        # self.assertFalse(data['success'])
        print(data)

    def test_delete_question(self):
        # add a queestion before deleting
        req = {
            'question':  'Heres a new question',
            'answer':  'Heres a new answer',
            'difficulty': 1,
            'category': 3,
        }

        res = self.client().post('/questions', json = req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # now delete a question
        ques_id = Question.query.first().id

        res = self.client().delete('/questions/' + str(ques_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_question_error_400(self):
        # delete a question
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


    # get questions by category
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()