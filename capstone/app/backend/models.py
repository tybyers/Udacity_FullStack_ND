import os
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db_filename = "database.db"
proj_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(proj_dir, db_filename))
#import db_defaults as DBDEF

KM_2_MILE = 0.621371

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    """
    Binds Flask app and SQLAlchemy service and initiates db

    Properties
    ----------
    app: Flask app
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    """
    Drops database tables, starts fresh with the following defaults
    """
    db.drop_all()
    db.create_all()
    # d1 = Distance(name = "Marathon", distance_km = 42.195)
    # d2 = Distance(name = "25K", distance_km = 25)
    # d3 = Distance(name = "12K", distance_km = 12)
    # r1 = Race(name = "MTC Marathon", city = "Minneapolis", state = "MN",
    #         website = "https://www.tcmevents.org/", distance_id = 1,
    #         date = datetime.strptime("2020-10-05", "%Y-%m-%d"))
    # db.session.add_all([d1, d2, d3, r1])
    # db.session.commit()

class Race(db.Model):
    """
    Name of foot race, location, distance, and date of competition
    """
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    website = Column(String)
    distance_id = Column(Integer, ForeignKey('distance.id'))
    date = Column(Date)

    def __init__(self, name, city, state, distance_id, website, date):
        self.name = name
        self.city = city
        self.state = state
        self.website = website
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
            'distance_id': self.distance_id,
            #distance_name = self.distance_name 
            'date': self.date,
            'website': self.website
        }

class Distance(db.Model):
    """
    Foot race distances
    """
    __tablename__ = 'distance'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    distance_km = Column(Float)
    distance_mi = Column(Float)
    races = db.relationship("Race", backref="distance")

    def __init__(self, name, distance_km):
        self.name = name
        self.distance_km = distance_km
        self.distance_mi = round(distance_km * KM_2_MILE, 2)

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
            'distance_km': self.distance_km,
            'distance_mi': self.distance_mi
        }