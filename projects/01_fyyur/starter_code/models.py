from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):

    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean, nullable=False, default=0)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    seeking_description = db.Column(db.String(500),nullable=False)
    show = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")
    def __repr__(self):
      return f'Venue<id: {self.id},name: {self.name},city: {self.city},state: {self.state},'+\
        f'address: {self.address},phone: {self.phone},image_link: {self.image_link},facebook_link: {self.facebook_link}>'

# # id,name,city,state,phone,genres,image_link,facebook_link
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_venue = db.Column(db.Boolean, nullable=False, default=0)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    
    show = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    def __repr__(self):
      return f'Artist<id = {self.id},name = {self.name},city = {self.city}\
        ,state = {self.state},phon = {self.phone},genres = {self.genres},image_link = {self.image_link}\
        ,facebook_link = {self.facebook_link}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.String, nullable=False)

  def __repr__(self):
      return f'Shows<id:{self.id}, artist_id: {self.artist_id}, venue_id: {self.venue_id}, start_time: {self.start_time}>'
