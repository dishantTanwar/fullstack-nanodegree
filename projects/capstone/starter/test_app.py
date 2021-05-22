import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, fill_dummy
from config import db_setup, bearer_tokens
# "postgresql://db_setup["user_name"]:dbsetup["password"]@{}/{}".format(db_setup["port"] db_setup["database_name_test"])

'''
### Database Setup
    With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
    ```bash
    psql [postgres_user] capstone_test_db < capstone_test_db.psql
    ```
'''

director = {
    'Authorization': bearer_tokens['director']
}

actor = {
    'Authorization': bearer_tokens['actor']
}





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
            # fill_dummy()

    
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

    '''
        GET /actors 
    '''
    # ROLE: public
    def test_add_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    '''
        GET /movies 
    '''
    # ROLE: public
    def test_get_movies(self):
        res =  self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    
    '''
        POST /actors 
    '''    

    #ROLE:  actor   
    def test_add_actor_by_actor(self):

        req = {
            'name' : 'RAM',
            'age' : 34
        } 

        res = self.client().post('/actors', json = req, headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    # ROLE: without authorization
    def test_add_actor_by_director(self):

        req = {
            'name' : 'RAM',
            'age' : 25
        } 

        res = self.client().post('/actors', json = req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    '''
        POST /movies 
    '''    

    # ROLE: actor   
    def test_add_movies_by_actor(self):

        req = {
            'title' : 'Deadpool',
            'genre' : 'action'
        } 

        res = self.client().post('/movies', json = req, headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
    
    # ROLE: director
    def test_add_movie_by_director(self):

        req = {
            'title' : 'Deadpool',
            'genre' : 'action'
        }  

        res = self.client().post('/movies', json = req, headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    '''
        PATCH /actors 
    '''    
    # ROLE: actor
    def test_update_actor(self):
        req = {
            'age' : 30
        } 
        res = self.client().patch('/actors/2', json = req, headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    # invalid id
    def test_update_actor_404(self):
        req = {
            'age' : 30
        } 
        res = self.client().patch('/actors/123412132', json = req, headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'] , 'resource not found')
    
    '''
        PATCH /movies 
    '''    
    # ROLE: director
    def test_edit_movie_bydict(self):
        req = {
            'genre' : 'horror'
        } 
        res = self.client().patch('/movies/2', json = req, headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # ROLE: actor
    def test_edit_movie_byactor(self):
        req = {
            'genre' : 'funny'
        } 
        res = self.client().patch('/movies/2', json = req, headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


    '''
        DELETE /movies 
    '''  
    # Role: actor
    def test_delete_movies_byactor(self):
        res = self.client().delete('/movies/1', headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message']['description'], 'Permission not found.')

    # ROLE: director
    def test_delete_movies_bydirector(self):
        res = self.client().delete('/movies/1', headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # ROLE: director     
    def test_delete_movies_valid_auth(self):
        res = self.client().delete('/actors/15122125', headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Resource id not found')

    '''
        DELETE /actors 
    '''  
    # ROLE: actor
    def test_delete_actors_byactor(self):
        res = self.client().delete('/actors/4', headers = actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # ROLE: director
    def test_delete_movies_director(self):
        res = self.client().delete('/actors/3', headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # ROLE: director     
    def test_delete_movies_valid_auth(self):
        res = self.client().delete('/actors/1512125', headers = director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()