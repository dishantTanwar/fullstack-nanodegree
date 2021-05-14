# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

```
# Full Stack Trivia API Backend

1.  [Start Project locally](#start-project)
2.  [API Documentation](#api-documentation)

<a name="start-project"></a>
## Start Project locally
Note: Before getting started, install the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/)

1. Move or `cd` into the backend folder

2. Create a virtualenv:
  ```bash
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ python -m venv ./venv 
  $ source venv/bin/activate
  ```
  This will create a virtual environment in your local mahine.
  - Tip: Always create a virtual environment for each project. It helps isolates the projects from system and other projects 

3. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

4. Start your postgres server and load the provided database.
```bash
$ createdb trivia
$ createdb trivia_test
$ psql trivia < trivia.psql
```

5. Run the development server:
  ```bash 
  $ export FLASK_APP=flaskr
  $ export FLASK_ENV=development # enables debug mode
  $ flask run
  ```


<a name="api-documentaton"></a>
## API Documentation

Now let's look at our `Endpoints` structure.

### Base URL

Our local app runs in at localhost on port 5000. To access our `API` flask should be running.

- I'll mention the `curl` commands to make requests but feel free to use `postman`
```
Our app's address is: 
[**_http://127.0.0.1:5000/_**]()
or
[**localhost:5000/**]()
```

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /questions    |  [x] |  [x]  |   [x]   |         
      /categories   |  [x] |       |         |           
      /quizzes      |      |  [x]  |         | 


### Working with endpoints

Click on a link to directly get to the ressource.

1. Questions
   1. [GET /questions](#get-questions)
   2. [POST /questions](#post-questions)
   3. [DELETE /questions/<question_id>](#delete-questions)
2. Quizzes
   1. [POST /quizzes](#post-quizzes)
3. Categories
   1. [GET /categories](#get-categories)
   2. [GET /categories/<category_id>/questions](#get-categories-questions)
# <a name="get-questions"></a>
### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 

#### Example response
```js
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
        [...]]
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}

```

# <a name="post-questions"></a>
### 2. POST '/questions'

Search Questions:
- Sends a post request in order to search for a specific question by search term 

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```
Request:
```js
{
    'searchTerm': 'this is the term the user is looking for'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
```js
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
```


**Insert related**

POST '/questions'
- Sends a post request in order to add a new question

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a question without an answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'
```
- Request Body: 
```js
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: Does not return any new data

# <a name="delete-questions"></a>
### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: 

#### Example response
```js
{
  "success": true
}
```

# <a name="post-quizzes"></a>
### 4. POST '/quizzes'
- Sends a post request in order to get the next question
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
Request Body: 
```js
{
    'previous_questions':  /*an array of question id's such as [1, 4, 20, 15] */
    'quiz_category': /*a string of the current category  eg. 2*/
}
```
- Returns: a single new question object 
```js
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```
# <a name="get-categories"></a>
### 5. GET '/categories'

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 


#### Example response
```js
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

# <a name="get-categories-questions"></a>
### 6. GET '/categories/${id}/questions'

- Fetches questions for a cateogry specified by id request argument 
```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string 
#### Example response

```js
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
        [...] 
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```




#### Example response
```js
{
  "deleted": 8,
  "success": true
}
```


