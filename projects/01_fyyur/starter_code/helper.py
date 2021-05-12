def create_artist_submission(db, Artist,obj):
  error = False
  try:
    name = obj['name']
    city = obj['city']
    state = obj['state']
    phone = obj['phone']
    genres = obj['genres']
    image_link = obj['image_link']
    facebook_link = obj['facebook_link']
    
    artist = Artist(name=name, city=city, state=state, phone=phone,\
      genres=genres, image_link=image_link, facebook_link=facebook_link )
    
    db.session.add(artist)
    db.session.commit()

  except:
    error = False  
    db.session.rollback()

  finally:
    db.session.close()
    if error: 
      print('An error occurred. Artist ' + name + ' could not be listed.')
    else:
      # on successful db insert, flash success
      print('Artist ' + name+ ' was successfully listed!')      

obj = {
  "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
    }


"""

data = db.session.query(Show.id,Show.start_time, Artist.name, Venue.name)\
      .join(Artist,Venue).all()
for d in data:
  print(d)
 
(1, '2021-05-12 01:52:59', 'Mason', 'Dishant Tanwar')
(2, '2021-05-12 01:54:58', 'Guns N Petals', 'test_name')
(3, '2021-05-12 01:54:58', 'Matt Quevedo', 'test_name')

"""
# from datetime import datetime
# def test(db, Artist, Show):
# data = []
# artist_id = 2
# obj = {}
# today = str(datetime.today())
# artist = Artist.query.get(artist_id)
# # shows = artist.show
# upcoming_shows = Show.query.filter(Show.artist_id == artist_id,Show.start_time >= today).all() 
# past_shows = Show.query.filter(Show.artist_id == artist_id,Show.start_time < today).all()
#     return (artist, upcoming_shows, past_shows)
from app import db, Venue, Show, Artist
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
    venue_obj['num_upcoming_shows'] = len(ven.show)
    venues.append(venue_obj)
  
  obj['venues'] = venues  
  
  data.append(obj)

for d in data:
  print(d)