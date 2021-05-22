import os, sys
import json
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from flask_moment import Moment
from flask_migrate import Migrate


from config import db_setup, SQLALCHEMY_TRACK_MODIFICATIONS

# database_name = "trivia"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = f'postgresql://{db_setup["user_name"]}:{db_setup["password"]}@{db_setup["port"]}/{db_setup["database_name_production"]}'


db = SQLAlchemy()
moment = Moment()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	moment.app = app
	db.init_app(app)
	Migrate(app, db)
    # db.create_all()
	# fill_dummy()

	# connect to a local postgresql database
# ---------------------------------------------------------
# Models.
# ---------------------------------------------------------

def create_default_actor():
	actor = Actor(name='Not disclosed',age='Not disclosed',gender='Not disclosed',msg_to_world='Not disclosed')
	try:
		actor.insert()
	except:
		print("Cannot create default actor data")

def fill_dummy():
	create_default_actor()
	num_actors = [Actor.query.all()]
	if not num_actors:
		create_default_actor()
	try:
		# actor = Actor(name='Popye',age='80',gender='male',msg_to_world='eat spinich')
		# actor.insert()
		# movie = Movie(title='Popye the sailorman', genre='action', release_date='26 jan 1985')
		# movie.insert()


		actor = Actor(name='Scarlett Johansson',age='36',gender='female',msg_to_world='The greatest glory in living lies not in never falling, but in rising every time we fall.')
		actor.insert()
		movie = Movie(title='Lucy', genre='sci-fi', release_date=' 25 July 2014')
		movie.insert()

		actor = Actor(name='Robert Downey, Jr',age='56',gender='male',msg_to_world='The lesson is that you can still make mistakes and be forgiven.')
		actor.insert()
		movie = Movie(title='Iron Man', genre='action', release_date='April 14, 2008 ')
		movie.insert()
	except:
		print("=============================================================")
		print("	dummy data error")
		db.session.close_all()
		print("=============================================================")


'''
	Actor

'''
class Actor(db.Model):  
	__tablename__ = 'actors'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	age = db.Column(db.String, nullable=True, default='Not disclosed')
	gender = db.Column(db.String, nullable=True, default='Not disclosed')
	msg_to_world = db.Column(db.String, nullable=True)

	# movie = db.relationship('Movie', backref='actor', lazy=True, cascade="all, delete") 

	def __init__(self, name, age, gender, msg_to_world):
		self.name = name
		self.age = age
		self.gender = gender
		self.msg_to_world = msg_to_world

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
		'id': self.id,
		'name': self.name,
		'age': self.age,
		'gender': self.gender,
		'msg_to_world': self.msg_to_world
		}
	def __repr__(self) :
		return f"<Actor id='{self.id}' name='{self.name}' msg_to_world='{self.msg_to_world}'>"


'''
Movie

'''
class Movie(db.Model):  
	__tablename__ = 'movies'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	genre = db.Column(db.String, nullable=True)
	release_date = db.Column(db.String, nullable=True)
	# actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id), nullable=False)

	def __init__(self, title, genre, release_date):
		self.title =  title	
		self.genre =  genre
		self.release_date =  release_date
		# self.actor_id = actor_id


	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
		'id': self.id,
		'title': self.title,
		'release_date': self.release_date,
		# 'actor' : self.actor.name,
		# 'actor_id' : self.actor_id
		}
	def __repr__(self) :
		return f"<Movie id='{self.id}' title='{self.title}' genre='{self.genre}' release_data='{self.release_date}' >"
