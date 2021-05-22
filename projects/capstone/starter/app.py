# ==============================================
# Imports
# ==============================================

import os
from flask_cors import CORS
from os import abort, error
from flask_moment import Moment
from flask_migrate import Migrate
from models import (
    db,
    # fill_dummy, 
    setup_db,
    Actor, 
    Movie)

from flask import (
    Flask,
    app, 
    request, 
    abort, 
    jsonify
    )   
from flask_sqlalchemy import SQLAlchemy

from auth.auth import AuthError, requires_auth

# ==============================================
# Config
# ==============================================


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
   # add CORS
#   cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# ==============================================
# Routes
# ==============================================

  
# --------------------------------------------
#  GET requests
# --------------------------------------------
    @app.route('/', methods = ['GET'])
    def root_index():
        return '<h1>Capstone APP running</h1>'

    '''
    @ implement endpoint
        GET /actors
            it should be a public endpoint
            it should contain only the actor.format() data representation
        returns status code 200 and json {"success": True, "actors": actors} 
        where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods = ['GET'])
    def get_actors():
        try:
            actors_query = Actor.query.all()
            actors = []
            for actor in actors_query:
                actors.append(actor.format())
            
            return jsonify({
                "success": True, 
                "actors": actors
                })
        except:
            abort(404, {'message' : 'unable to get actors'})

    '''
    @TODO implement endpoint
        GET /actormovie
            it should be a public endpoint
            it should contain only the movie.format() data representation
        returns status code 200 and json {"success": True, "movies": movies} 
        where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods = ['GET'])
    def get_movies():
        try:
            movies_query = Movie.query.all()
            movies = []
            for movie in movies_query:
                movies.append(movie.format())
            
            return jsonify({
                "success": True, 
                "movies": movies
                })
        except:
            abort(404, {'message' : 'unable to get movies'})


    # --------------------------------------------
    #  POST requests
    # --------------------------------------------
    '''
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:actors' permission
            it should contain the actor.info() data representation
        returns status code 200 and json {"success": True, "actors": actor} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''

    @app.route('/actors', methods = ['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        new_actor = request.get_json()

        name = new_actor.get('name', None)
        age = new_actor.get('age', None)
        gender = new_actor.get('gender', None)
        msg_to_world = new_actor.get('msg_to_world', None)
        
        # only verifying name because others have a default value of 'Not disclosed'
        if not name:
            abort(400, {'message' : 'actor name missing from request'})


        actor = Actor(name=name, age=age, gender=gender, msg_to_world=msg_to_world)
        try:
            actor.insert()
            return jsonify({
                "success" : True,
                "id" : actor.id
            })
        except:
            abort(500, {'message' : 'coulded save to database'})

    '''
    @TODO implement endpoint
        POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission
            it should contain the movie.format() data representation
        returns status code 200 and json {"success": True, "movies": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''

    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        new_movie = request.get_json()

        title = new_movie.get('title', None)
        genre = new_movie.get('genre', None)
        release_date = new_movie.get('release_date', None)
        # actor_id = new_movie.get('actor_id', None)

        if not title:
            abort(400, {'message' : 'movie title missing from request'})

        # if not actor_id:
        #     actor_id = 0
        
        movie = Movie(title=title,genre =genre,release_date=release_date)
            
        try:
            movie.insert()
            return jsonify({
                "success" : True,
                "movie" : movie.id
            })
        except:
            abort(500, {'message' : 'coulded save to database'})
            




    # --------------------------------------------
    #  PATCH requests
    # --------------------------------------------  
        '''          
    @TODO implement endpoint
    PATCH /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
        it should contain the actor.format() data representation
    returns status code 200 and json {"success": True, "actors": drink} 
        where movie an array containing only the updated actor
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:id>', methods = ['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):

        body = request.get_json()

        if not body:
            abort(400,{'message' : 'Bad Request, no content in request body'})

        actor = Movie.query.get_or_404(id, {'message' : 'Resource id not found.'})

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_msg_to_world = body.get('msg_to_world', None)

        flag = True
        if new_name:
            actor.title = new_name
            flag = False

        if new_age:
            actor.age = new_age
            flag = False

        if new_gender:
            actor.gender = new_gender
            flag = False

        if new_msg_to_world:
            actor.msg_to_world = new_msg_to_world
            flag = False

        if flag:
            abort(400, {'message' : 'bad request, invalid request body'})
        
        try :
            actor.update()
            return jsonify({
                "success": True, 
                "actor": actor.format() 
            })

        except:
            abort(404, {'500' : 'unable to update resource'})
    '''
    @TODO implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the movie.format() data representation
        returns status code 200 and json {"success": True, "movies": drink} 
            where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:id>', methods = ['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):

        body = request.get_json()

        if not id:
            abort(404)
        if not body:
            abort(400,{'message' : 'Bad Request, no content in request body'})

        movie = Movie.query.get_or_404(id, {'message' : 'Resource id not found.'})

        new_title = body.get('title', None)
        new_genre = body.get('genre', None)
        new_release_date = body.get('release_date', None)
        # new_actor_id = body.get('actor_id', None)

        flag = True
        if new_title:
            movie.title = new_title
            flag = False

        if new_genre:
            movie.genre = new_genre
            flag = False

        if new_release_date:
            movie.release_date = new_release_date
            flag = False

        # if new_actor_id:
        #     movie.actor_id = new_actor_id
        #     flag = False
        
        if flag:
            abort(400, {'message' : 'bad request, invalid request body'})
        
        try :
            movie.update()
            return jsonify({
                "success": True, 
                "movies": [movie.format()]})

        except:
            abort(500, {'500' : 'unable to update resource'})


    # --------------------------------------------
    #  DELETE requests
    # --------------------------------------------
    '''
    @TODO implement endpoint
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:id>', methods = ['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):

        actor = Actor.query.get_or_404(id, {'message' : 'Resource id not found'})
        
        try :
            actor.delete()
            return jsonify({
                "success": True, 
                "delete": actor.id
                })

        except:
            abort(500, {'message' : 'unable to delete resource'})
            
    '''
    @TODO implement endpoint
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:id>', methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):

        movie = Movie.query.get_or_404(id, {'message' : 'Resource id not found'})
        
        try :
            movie.delete()
            return jsonify({
                "success": True, 
                "delete": movie.id
                })

        except:
            abort(500, {'message' : 'unable to delete resource'})

    # ==============================================
    # Error Handling
    # ==============================================


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": 'bad request'
                        }), 400

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
                        "success": False, 
                        "error": AuthError.status_code,
                        "message": AuthError.error
                        }), AuthError.status_code

    return app




# ==============================================
# Launch
# ==============================================
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

