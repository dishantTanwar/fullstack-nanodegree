#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import date, timezone, datetime 
import time
  
import json
from os import abort
import sys
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
  )
import flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import FlaskForm as Form
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from wtforms import meta
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
# db = SQLAlchemy(app)

# connect to a local postgresql database
migrate = Migrate(app, db)

def give_app():
  """
    Use app in python terminal
    
  """
  app.app_context().push()
  return app

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  
  citi_state_list = db.session.query(Venue.city, Venue.state).distinct().all()
  for city, state in citi_state_list:
    obj = {}
    venues = []

    obj['city'] = city
    obj['state'] = state

    for ven in Venue.query.filter(Venue.city == city).all():
      venue_obj = {}
      venue_obj['id'] = ven.id
      venue_obj['name'] = ven.name
      venues.append(venue_obj)
      upcoming_shows = Show.query.filter(Show.venue_id == ven.id\
                    ,Show.start_time >= str(datetime.today())).all() 

      venue_obj['num_upcoming_shows'] = len(upcoming_shows)
    
    obj['venues'] = venues  
    
    data.append(obj)

  return  render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term', '')
  response = {}
  data = []
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  for venue in venues:
    obj = {}
    num_upcoming_shows = len(Show.query.filter(Show.venue_id == venue.id\
                            , Show.start_time > str(datetime.today())\
                            ).all())
    obj['id'] = venue.id
    obj['name'] = venue.name
    obj['num_upcoming_shows'] = num_upcoming_shows
    data.append(obj)
  
  response['count'] = len(venues)
  response['data'] = data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  """
  # Doing it the LAZY = True way (relationship)

      today = str(datetime.today())
      venue = Venue.query.get(venue_id)
      # shows = artist.show
      upcoming_shows = Show.query.filter(Show.venue_id == venue_id\
                        ,Show.start_time >= today).all() 
      past_shows = Show.query.  filter(Show.venue_id == venue_id\
                    ,Show.start_time < today).all()
      
      # genres =  ''.join(venue.genres)
      data = {}
      data["id"] = venue.id
      data["name"] = venue.name
      data["genres"] = venue.genres
      data["city"] = venue.city
      data["state"] =venue.state
      data["phone"] = venue.phone
      data["seeking_talent"] =venue.seeking_talent
      data["image_link"] = venue.image_link
      data["upcoming_shows"] = upcoming_shows
      data["past_shows"] = past_shows
  """
  # Lazy =  'joined' 
  """  
  Now, your query venue.shows, for example, will produce something like this:

  SELECT 
      shows.id,
      ...,
      artists.id,
      ...,
      venues.id,
      ...,
      ...
      FROM shows
      LEFT OUTER JOIN artists
          ON artists.id = shows.artist_id
      LEFT OUTER JOIN venues 
          ON venues.id = shows.venue_id"""
          
  venue = Venue.query.get(venue_id)

  """
  ### WITHOUT using JOINS

  past_shows = []
  upcoming_shows = []
  
  for show in venue.show:
    temp_show = {
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time
    }
        if str(show.start_time) <= str(datetime.now()):
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)
  """
 
  ### USING JOINS
  past_shows_query =  db.session.query(Show) \
                      .join(Venue) \
                      .filter(Show.venue_id == venue_id) \
                      .filter(Show.start_time < str(datetime.now())) \
                      .all()
                    
  upcoming_shows_query = db.session.query(Show) \
                         .join(Venue) \
                         .filter(Show.venue_id == venue_id) \
                         .filter(Show.start_time >= str(datetime.now())) \
                         .all()
  # Get past show data to be sent to front end
  past_shows = []
  for show in past_shows_query:
    temp_show = {
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time
    }
    past_shows.append(temp_show)

  # Get upcoming show data to be sent to front end
  upcoming_shows = []
  for show in upcoming_shows_query:
    temp_show = {
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time
    }
    past_shows.append(temp_show)
 
  

  # object class to dict
  data = vars(venue)
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  form = VenueForm(request.form, meta={'csrf' : False})
  if form.validate():
    try:
      """ WAY 1: but can be improved with FlaskForm
      name  = request.form.get('name')
      city  = request.form.get('city')
      state  = request.form.get('state')
      address  = request.form.get('address')
      phone  = request.form.get('phone')
      image_link  = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      seeking_talent = int(bool(request.form.get('seeking_talent')))
      genres = request.form.getlist('genres')
      
      seeking_description = request.form.get('seeking_description')

      venue = Venue(name=name ,city=city ,state=state ,address=address ,phone=phone \
        ,image_link =image_link,facebook_link=facebook_link \
        ,seeking_talent=seeking_talent, genres=genres, seeking_description=seeking_description)
      
    """

    # BETTER WAY
    # Create using FlaskForm
    # To avoid having to deal with each field manually, 
    #  you can use the form.populate_obj() method:
      form = VenueForm(request.form)
      venue = Venue()
      form.populate_obj(venue)
      

      # Commit to database
      db.session.add(venue)
      db.session.commit()
      print('----------ADD VENUE: Success-----------')

    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

    finally:
      db.session.close()
      if error:
        print('-------- ADD Venue: Fail --------')
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    # on successful db insert, flash success
      flash('Venue ' + form.name.data + ' was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '| '.join(err))
    flash('Errors ' + str(message))
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  query = db.session.query(Artist.id, Artist.name).all()

  for val in query:
    temp = {}
    temp['id'] = val.id
    temp['name'] = val.name
    data.append(temp)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
 
  search_term = request.form.get('search_term', '')
  response = {}
  data = []
  artists = Artist.query.filter(Artist.name.like(f'%{search_term}%')).all()
  for artist in artists:
    obj = {}
    num_upcoming_shows = len(Show.query.filter(Show.artist_id == artist.id\
                            , Show.start_time > str(datetime.today())\
                            ).all())
    obj['id'] = artist.id
    obj['name'] = artist.name
    obj['num_upcoming_shows'] = num_upcoming_shows
    data.append(obj)
  
  response['count'] = len(artists)
  response['data'] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artist table, using artist_id
  """
    THE 
      laze = true 
    WAY

    today = str(datetime.today())
    artist = Artist.query.get(artist_id)
    # shows = artist.show
    upcoming_shows = Show.query.filter(Show.artist_id == artist_id\
                      ,Show.start_time >= today).all() 
    past_shows = Show.query.filter(Show.artist_id == artist_id\
                  ,Show.start_time < today).all()
    
    data = {}
    data["id"] = artist.id
    data["name"] = artist.name

    genres =  ''.join(artist.genres)
    # data["genres"] = genres
    data["genres"] = artist.genres

    data["city"] = artist.city
    data["state"] = artist.state
    data["phone"] = artist.phone
    data["seeking_venue"] = artist.seeking_venue
    data["image_link"] = artist.image_link
    data["upcoming_shows"] = upcoming_shows
    data["past_shows"] = past_shows"""
  """
  ### Without using JOINS
  artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  for show in artist.show:
    temp_show = {
      'venue_id' : show.venue_id,
      'venue_name' : show.venue.name,
      'venue_image_link' : show.venue.image_link,
      'start_time' : show.start_time
    }
    if str(show.start_time) <= str(datetime.now()):
      past_shows.append(temp_show)
    else:
      upcoming_shows.append(temp_show)
  """

  ### Using JOINS
  artist = Artist.query.get(artist_id)

  past_shows_query =  db.session.query(Show) \
                      .join(Artist) \
                      .filter(Show.venue_id == artist_id) \
                      .filter(Show.start_time < str(datetime.now())) \
                      .all()
                    
  upcoming_shows_query = db.session.query(Show) \
                         .join(Artist) \
                         .filter(Show.venue_id == artist_id) \
                         .filter(Show.start_time >= str(datetime.now())) \
                         .all()
  # Get past show data to be sent to front end
  past_shows = []
  for show in past_shows_query:
    temp_show = {
      'venue_id' : show.venue_id,
      'venue_name' : show.venue.name,
      'venue_image_link' : show.venue.image_link,
      'start_time' : show.start_time
    }
    past_shows.append(temp_show)

  # Get upcoming show data to be sent to front end
  upcoming_shows = []
  for show in upcoming_shows_query:
    temp_show = {
      'venue_id' : show.venue_id,
      'venue_name' : show.venue.name,
      'venue_image_link' : show.venue.image_link,
      'start_time' : show.start_time
    }
    past_shows.append(temp_show)
  # object class to dict
  data = vars(artist)
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name  = request.form.get('name')
    artist.city  = request.form.get('city')
    artist.state  = request.form.get('state')
    artist.address  = request.form.get('address')
    artist.phone  = request.form.get('phone')
    artist.image_link  = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.seeking_talent = int(bool(request.form.get('seeking_talent')))
    artist.genres = request.form.getlist('genres')
    
    artist.seeking_description = request.form.get('seeking_description')

    db.session.add(artist)
    db.session.commit()
    print('----------EDIT Artist: Success-----------')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
      print('-------- EDIT Artist: Fail --------')
      flash('An error occurred. Artist could not be edited.')
  # on successful db insert, flash success
    flash('Artist was successfully edited!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # populate form with values from venue with ID <venue_id>
  """
    Way 1: not so smart
    
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
  """   

  ## BETTER WAY
  # pre-populate a form with values retrieved from the database
  venue = Venue.query.filter(Venue.id == venue_id).first_or_404()
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.get(venue_id)
    venue.name  = request.form.get('name')
    venue.city  = request.form.get('city')
    venue.state  = request.form.get('state')
    venue.address  = request.form.get('address')
    venue.phone  = request.form.get('phone')
    venue.image_link  = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')
    venue.seeking_talent = int(bool(request.form.get('seeking_talent')))
    venue.genres = request.form.getlist('genres')
    
    venue.seeking_description = request.form.get('seeking_description')

    db.session.add(venue)
    db.session.commit()
    print('----------EDIT Venue: Success-----------')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
      print('-------- EDIT Venue: Fail --------')
      flash('An error occurred. Venue could not be edited.')
  # on successful db insert, flash success
    flash('Venue was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  error = False
  form  = VenueForm(request.form, meta={'csfr' : False})
  if form.Validate():
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      seeking_venue = int(bool(request.form.get('seeking_venue')))
      seeking_description = request.form.get('seeking_description')
      
      artist = Artist(name=name, city=city, state=state, phone=phone,\
        genres=genres, image_link=image_link, facebook_link=facebook_link \
        ,seeking_venue=seeking_venue \
        ,seeking_description=seeking_description)
      
      db.session.add(artist)
      db.session.commit()

    except:
      error = True  
      db.session.rollback()
      print(sys.exc_info())

    finally:
      db.session.close()
      if error: 
        flash('self defined error ' + name + ' could not be listed.')
        abort(400)
      else:
        # on successful db insert, flash success
        flash('Artist ' + name+ ' was successfully listed!')  
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '| '.join(err))
    flash('Errors ' + str(message))
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  data = []

  query = Show.query.all()
  for q in query:
    obj = {}
    obj['venue_id'] = q.venue_id
    obj['venue_name'] = q.venue.name
    obj['artist_id'] = q.artist.id
    obj['artist_name'] = q.artist.name
    obj['artist_image_link'] = q.artist.image_link
    obj['start_time'] = q.start_time
    data.append(obj)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  error = False
  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate():

    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')

      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)

      db.session.add(show)
      db.session.commit()
    
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    
    finally:
      db.session.close()
      if error:
        flash('An error occurred. Show could not be listed.')
        abort(400)
      else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '| '.join(err))
    flash('Errors ' + str(message))

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
