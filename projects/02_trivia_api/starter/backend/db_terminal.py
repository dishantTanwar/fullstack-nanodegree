from flaskr.__init__ import create_app #, Question, Category
from models import Question, Category, db

app = create_app()
app.app_context()

"""

from db_terminal import Question, db, Category

"""