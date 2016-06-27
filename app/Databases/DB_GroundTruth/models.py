from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class GTdata(db.Model):
    __tablename__ = 'GroundTruthData'
    room = db.Column(db.String(10), db.ForeignKey('Logs.room'))
    capacity = db.Column(db.Integer)
    time = db.Column(db.DataTime)
    occupancyPercent = db.Column(db.Integer)    # % occupancy of room
    occupancy = db.Column(db.Integer)           # occupancy count

    def __init__(self, room, capacity, time, occupancy):
        self.room = room
        self.capacity = capacity
        self.time = time
        self.occupancy = occupancy

    def __repr__(self):
        return '<User %r>' % self.room





#http://flask-sqlalchemy.pocoo.org/2.1/models/
