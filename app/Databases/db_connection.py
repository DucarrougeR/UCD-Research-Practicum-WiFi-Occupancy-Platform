#Romain Ducarrouge
from flask import Flask
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, String, Column
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)

# create the Database with 3 tables
class Class(db.Model):
    __tablename__ = 'class'
    module = Column(String(20), primary_key=True, nullable=False)
    size = Column(Integer)
    room = Column(String(6))
    day = Column(String(4))
    time = Column(DateTime)
    date = Column(Integer)
    month = Column(String)
    lecture = Column(Boolean, default=True)

    def __init__(self, module, size, room, day, time, date, month):
        self.module = module
        self.size = size
        self.room = room
        self.day = day
        self.time = time
        self.date = date
        self.month = month

    def __repr__(self):
        return "<Class module='%s', size='%d', room='%s'>" % (self.module, self.size, self.room)
################################################################################

class Building(db.Model):
    __tablename__ = 'building'
    room = db.Column(db.String(6), primary_key=True, nullable=False)
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
    day = db.Column(db.String(6))
    month = db.Column(db.String(6))
    date = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    year = db.Column(db.Integer)
    associated = db.Column(db.Integer)
    authenticated = db.Column(db.Integer)
    occupancy = db.Column(db.String)
    occupancyCount = db.Column(db.Integer)

    def __init__(self, room, day, month, date, time, year, associated, authenticated, occupancy, occupancyCount):
        self.room = room
        self.day = day
        self.month = month
        self.date = date
        self.time = time
        self.year = year
        self.associated = associated
        self.authenticated = authenticated
        self.occupancy = occupancy
        self.occupancyCount = occupancyCount

    def __repr__(self):
        return "<Counts room='%s', associated='%d', authenticated='%d', occupancyCount='%d')>" % (self.room, self.associated, self.authenticated, self.occupancyCount)
################################################################################



# def setup():
#     engine = create_engine('sqlite:///./datebase.db', echo=True)
#     if not database_exists(engine.url):
#         create_database(engine.url)
#     connection = engine.connect()
#     Base.metadata.create_all(connection, bind=engine)


# def teardown():
#
# def test_connection():

'''sources
engine creation: http://docs.sqlalchemy.org/en/latest/core/engines.html
video for SQLAlchemy https://www.youtube.com/watch?v=f_-ApViOv20
'''