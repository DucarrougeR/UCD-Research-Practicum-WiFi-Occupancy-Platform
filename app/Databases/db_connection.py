#Romain Ducarrouge
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import session
from db import model

Base = declarative_base()

# create the Database
# create the tables for Logs and for Ground Truth data
# use Room Number as Foreign Key for 2 tables

class Logs(db.Model):
    __tablename__ = 'Logs'
    campus = db.Column(db.String(20))
    building = db.Column(db.String(20), primary_key=True)
    room = db.Column(db.String(10), primary_key=True, db.ForeignKey)
    date = db.Column(db.DateTime)
    associated = db.Column(db.Integer)
    authenticated = db.Column(db.Integer)

    def __init__(self, campus, building, room, date, associated, authenticated):
        self.campus = campus
        self.building = building
        self.room = room
        self.date = date
        self.associated = associated
        self.authenticated = authenticated

    def __repr__(self):
        return '<User %r>' % self.room
################################################################################

class GTdata(db.Model):
    __tablename__ = 'GroundTruthData'
    room = db.Column(db.String(10), db.ForeignKey('Logs.room'))
    capacity = db.Column(db.Integer)
    time = db.Column(db.DataTime)
    occupancy = db.Column(db.Integer)

    def __init__(self, room, capacity, time, occupancy):
        self.room = room
        self.capacity = capacity
        self.time = time
        self.occupancy = occupancy

    def __repr__(self):
        return '<User %r>' % self.room
################################################################################

def setup():
    engine = create_engine('sqlite:///./datebase.db', echo=True)
    connection = engine.connect()
    Base.metadata.create_all(connection, bind=engine)


def teardown():
    session.remove

def test_connection():

'''sources
engine creation: http://docs.sqlalchemy.org/en/latest/core/engines.html
video for SQLAlchemy https://www.youtube.com/watch?v=f_-ApViOv20
'''