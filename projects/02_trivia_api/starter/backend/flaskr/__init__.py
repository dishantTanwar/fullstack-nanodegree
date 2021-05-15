import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import Pagination, SQLAlchemy
from sqlalchemy.sql.sqltypes import JSON
from flask_cors import CORS, cross_origin
import sys
import random
from math import ceil

# import os,sys,inspect
sys.path.insert(0, '..')
# from .. import models 
from models import setup_db, Question, Category, db


""""""""""""""""""""""""""""""""""" 
Global variables & functions
"""""""""""""""""""""""""""""""""""
QUESTIONS_PER_PAGE = 10

def get_categories_dict():
  categories = {}
  category_query = Category.query.all()
  for cat in  category_query:
    categories[cat.id] = cat.type  
  return categories

""""""""""""""""""""""""""""""""""" 
 Flask APP
"""""""""""""""""""""""""""""""""""
def create_app(test_config=None):

  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
 
  # add CORS
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
     response.headers.add('Access-Control-Allow-Headers',  \
                          'Content-Type,Authorization,true')

     response.headers.add('Access-Control-Allow-Methods', \
                          'GET,PATCH,POST,DELETE,OPTIONS')
     return response
  

  # an endpoint to get all categories
  @app.route('/categories', methods= ['GET'])
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
    response = {
      'success' : True,
      'categories': get_categories_dict()
    }

    return jsonify(response)


  # an endpoint to paginated set of questions
  @app.route('/questions', methods = ['GET'])
  def show_questions():
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
    page = int(request.args.get('page', default=1))
    max_page_nums = ceil(len(Question.query.all()) / QUESTIONS_PER_PAGE)
    if page <= 0 or page >= max_page_nums:
      abort(400)
    else: 
      # Paginate Questions in a set of 10
      pagination_obj = Question.query.order_by(Question.id) \
                      .paginate(page=page, per_page=QUESTIONS_PER_PAGE)
      questions = []
      for question in pagination_obj.items:
        questions.append(question.format())
      
      response = {
          'success' : True,
          'questions': questions,
          'total_questions': len(Question.query.all()),
          'categories': get_categories_dict(),
          'current_category': 'History'
      }

      return jsonify(response)

  
  # an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    """
      DELETE '/questions/${id}'
    - Deletes a specified question using the id of the question
    - Request Arguments: id - integer
    - Returns: Does not need to return anything besides the appropriate HTTP status code. 
        Optionally can return the id of the question. If you are able to modify the frontend, 
        you can have it remove the question using the id instead of refetching the questions. 
    
    """
    question = Question.query.get_or_404(question_id,{'message' : f'Cannot find Question wihd id = {question_id}'} )

    
    try:
      question.delete()
      return jsonify({
        'success' : True
      })

    except:
      db.session.rollback()
      print('Error', sys.exc_info())
      abort(404, {'message' : 'question deletion failed'})

    finally:
      db.session.close()


  # an endpoint to POST a new question or query questions with search_term 
  @app.route('/questions', methods = ['POST'])
  def create_or_search_question():
    
    error = False
    body = request.get_json()

    search_term = body.get('searchTerm', None)
    if search_term:
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
      search_result = Question.query \
                      .filter(Question.question.ilike(f'%{search_term}%')) \
                      .all()

      questions = []
      for question in search_result:
        questions.append(question.format())
      
      response = {
        'success' : True,
        'questions': questions,
        'total_questions': len(Question.query.all()),
        'current_category': 'Entertainment'
      }

      return jsonify(response)
    
    else:
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
      # Add new question to database
      question   =  body.get('question', None),
      answer     =  body.get('answer', None),
      difficulty =  body.get('difficulty', None),
      category   =  body.get('category', None)

      if not question:
        abort(400, {'message': 'Question not found in request'})

      if not answer:
        abort(400, {'message': 'Answer not found in request'})

      if not category:
        abort(400, {'message': 'Category not found in request'})

      if not difficulty:
        abort(400, {'message': 'Difficulty not found in request'})
      
      try:
        # Initialize Question Model
        new_question = Question(
          question =question,
          answer =answer,
          difficulty =difficulty,
          category =category
        )
        
        # add to database
        new_question.insert()
        return jsonify({
          "success" : True
        })
      
      except:
        error = True
        db.session.rollback()
        print('Error', sys.exc_info())
        abort(500, {'message' : 'had to rollback database'})
      
      finally:
        db.session.close()


  #  Create a GET endpoint to get questions based on category. 
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_by_category(category_id):
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
    ques_query = Question.query.filter(Question.category == category_id) \
                .all()

    questions = []
    for question in ques_query:
      questions.append(question.format())
    
    response = {
        'success' : True,
        'questions': questions,
        'total_questions': len(Question.query.all()),
        'current_category': 'History'
    }

    return jsonify(response)       


  # a POST endpoint to get questions to play the quiz. 
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

    request_data = request.get_json()
    prev_questions = request_data.get('previous_questions', [])
    quiz_category = request_data.get('quiz_category', None)

    if not quiz_category:
      abort(400)

    question = Question.query.filter( \
                  Question.category == quiz_category['id'], \
                  Question.id.notin_(prev_questions)) \
                  .first()

    response = {
      # 'success' : True,
      'question': question.format()
    }
    return jsonify(response)

    
  # error handlers for all expected errors 
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": "400",
      "message": error.description
      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
    return jsonify({
      "success": False, 
      "error": "404",
      "message": error.description
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": "405",
      "message": error.description
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": "422",
      "message": error.description
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": "500",
      "message": error.description
      }), 500
  
  return app


