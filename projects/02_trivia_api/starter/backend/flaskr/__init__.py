import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import Pagination, SQLAlchemy
from sqlalchemy.sql.sqltypes import JSON
from flask_cors import CORS
import sys
import random


# import os,sys,inspect
# sys.path.insert(0, '..')
# from .. import models
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#################### SHIFT + Enter ##########
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources = {r"/*" : {"origins" : "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
     response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
     return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods= ['GET'])
  # @cross_origin()
  def show_categories():
    """ 
    GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids 
      and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key ie. categories,
              that contains an object of 
              id: category_string key:value pairs. 
    {
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" }
    }
    """
#%%
    response = {
      'categories': {} 
    }
    print("Hello world")
    category_query = Category.query.all()
    for cat in  category_query:
      response['categories'][cat.id] = cat.type
# %%

    return jsonify(response)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions?page=<int:page>}', methods = ['GET'])
  def show_questions(page):
    """
      GET '/questions?page=${integer}'
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
    - Request Arguments: page - integer
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
      {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 2
            },
            ... # 10 questions
        ],
        'totalQuestions': 100,
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" },
        'currentCategory': 'History'
      }
    """
    # Paginate Questions in a set of 10
    pagination_obj = Question.query.paginate(page=page, per_page=10)
    questions = []
    for question in pagination_obj.items:
      questions.append(question.format())
    
    response = {
        'questions': questions,
        'totalQuestions': len(Question.query.all()),
        # 'categories': { '1' : "Science",
        # '2' : "Art",
        # '3' : "Geography",
        # '4' : "History",
        # '5' : "Entertainment",
        # '6' : "Sports" },
        'currentCategory': 'History'
    }

    return jsonify(response)
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  app.route('/questions/${id}', methods = ['DELETE'])
  def delete_question(question_id):
    """
      DELETE '/questions/${id}'
    - Deletes a specified question using the id of the question
    - Request Arguments: id - integer
    - Returns: Does not need to return anything besides the appropriate HTTP status code. 
        Optionally can return the id of the question. If you are able to modify the frontend, 
        you can have it remove the question using the id instead of refetching the questions. 
    
    """
    pass


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def create_question():
    """
      POST '/questions'
      - Sends a post request in order to add a new question
      - Request Body: 
      {
          'question':  'Heres a new question string',
          'answer':  'Heres a new answer string',
          'difficulty': 1,
          'category': 3,
      }
      - Returns: Does not return any new data
    """
    pass


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods = ['POST'])
  def search_question(term):
    """
      POST '/questions'
      - Sends a post request in order to search for a specific question by search term 
      - Request Body: 
      
      {
          'searchTerm': 'this is the term the user is looking for'
      }
     
      - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
      {
          'questions': [
              {
                  'id': 1,
                  'question': 'This is a question',
                  'answer': 'This is an answer', 
                  'difficulty': 5,
                  'category': 5
              },
          ],
          'totalQuestions': 100,
          'currentCategory': 'Entertainment'
      }
    """
    pass


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  app.route('/categories/${id}/questions', methods=['GET'])
  def get_question_by_category(cat_id):
    """
    GET '/categories/${id}/questions'
      - Fetches questions for a cateogry specified by id request argument 
      - Request Arguments: id - integer
      - Returns: An object with questions for the specified category, total questions, and current category string 
      {
        'questions': [
          {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
          },
        ],
        'totalQuestions': 100,
        'currentCategory': 'History'
      }
    """
    pass


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def next_question():
    """
    POST '/quizzes'
    - Sends a post request in order to get the next question 
    - Request Body: 
    {
      'previous_questions':  an array of question id's such as [1, 4, 20, 15]
      'quiz_category': a string of the current category 
    }
    - Returns: a single new question object 
    {
      'question': {
          'id': 1,
          'question': 'This is a question',
          'answer': 'This is an answer', 
          'difficulty': 5,
          'category': 4
      }
    }
    """
    pass

  

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

# %%
