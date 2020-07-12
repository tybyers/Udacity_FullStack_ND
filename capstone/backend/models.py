import os
from sqlalchemy import Column, String, Integer, relationship, backref, Float, Date
from flask_sqlalchemy import SQLAlchemy
import json

db_filename = "database.db"
proj_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(proj_dir, db_filename))

db = SQLAlchemy()

def setup_db(app):
    """
    Binds Flask app and SQLAlchemy service and initiates db

    Properties
    ----------
    app: Flask app
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    """
    Drops database tables, starts fresh
    """
    db.drop_all()
    db.create_all()

class Race(db.Model):
    """
    Name of foot race, location, distance, and date of competition
    """
    __tablename__ = 'races'

    id = Column(Integer, primary_key=True)
    name = Column(string)
    city = Column(string)
    state = Column(string)
    distance_id = Column(Integer, ForeignKey('distance.id'))
    distance_name = relationship('Distance', back_populates="name"))
    date = Column(Date)

    def __init__(self, name, city, state, distance_id, date):
        self.name = name
        self.city = city
        self.state = state
        self.distance_id = distance_id
        self.date = date

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
            'city': self.city,
            'state': self.state,
            'distance_id' = self.distance_id,
            #distance_name = self.distance_name 
            'date' = self.date
        }

class Distance(db.Model):
    """
    Foot race distances
    """
    id = Column(Integer, primary_key=True)
    name = Column(string)
    distance_km = Column(Float)
    distance_mi = Column(Float)

    def __init__(self, name, distance_km):
        self.name = name
        self.distance_km = distance_km
        self.distance_mi = distance_km * 0.621371

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance_km': self.distance_km,
            'distance_mi': self.distance_mi
        }