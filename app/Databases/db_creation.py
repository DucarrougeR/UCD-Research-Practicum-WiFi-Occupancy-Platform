#Romain Ducarrouge
# from flask import Flask
# from sqlalchemy import *

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Tells SQLAlchemy the path to the database and the username and passwords
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:////tmp/app/Databases/database.db'
db = SQLAlchemy(app)

# create the Database with 3 tables
class Class(db.Model):
    __tablename__ = 'class'
    module = db.Column(db.String(20), primary_key=True, nullable=False)
    size = db.Column(db.Integer)
    room = db.Column(db.String(6))
    timeStamp = db.Column(db.DateTime)
    lecture = db.Column(db.Boolean, default=True)
    building = db.relationship('Building', backref='Class', lazy='dynamic')
    counts = db.relationship('Counts', backref='Class', lazy='dynamic')

    def __init__(self, module, size, room, timeStamp, lecture):
        self.module = module
        self.size = size
        self.room = room
        self.timeStamp = timeStamp
        self.lecture = lecture

    def __repr__(self):
        return "<Class module='%s', size='%d', room='%s'>" % (self.module, self.size, self.room)
################################################################################

class Building(db.Model):
    __tablename__ = 'building'
    room = db.Column(db.String(6), primary_key=True, nullable=False, unique=True)
    campus = db.Column(db.String(6))
    building = db.Column(db.String(6))
    capacity = db.Column(db.Integer)
    classRoom = db.Column(db.Integer, db.ForeignKey('class.room'))

    def __init__(self, room, campus, building, capacity):
        self.room = room
        self.campus = campus
        self.building = building
        self.capacity = capacity

    def __repr__(self):
        return "<Building room='%s', campus='%s', building='%s', capacity='%d')>" % (self.room, self.campus, self.building, self.capacity)
################################################################################

class Counts(db.Model):
    __tablename__ = 'counts'
    room = db.Column(db.String(6), db.ForeignKey('building.room'), nullable=False)
    timestamp = db.Column(db.DateTime)
    associated = db.Column(db.Integer)
    authenticated = db.Column(db.Integer)
    occupancy = db.Column(db.String(6))
    occupancyCount = db.Column(db.Integer)

    def __init__(self, room, timestamp, associated, authenticated, occupancy, occupancyCount):
        self.room = room
        self.timestamp = timestamp
        self.associated = associated
        self.authenticated = authenticated
        self.occupancy = occupancy
        self.occupancyCount = occupancyCount

    def __repr__(self):
        return "<Counts room='%s', associated='%d', authenticated='%d', occupancyCount='%d')>" % (self.room, self.associated, self.authenticated, self.occupancyCount)
################################################################################


'''sources
engine creation: http://docs.sqlalchemy.org/en/latest/core/engines.html
video for SQLAlchemy https://www.youtube.com/watch?v=f_-ApViOv20
GitHub repo for Flaskr tutorial to flask and sql
'''