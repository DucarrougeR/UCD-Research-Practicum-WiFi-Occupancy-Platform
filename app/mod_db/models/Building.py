# Luke Kearney
from app.mod_db import db

class Building(db.Model):
    __tablename__ = 'building'
    room = db.Column(db.String(5), primary_key=True)
    building = db.Column(db.String(100))
    campus = db.Column(db.String(100))
    capacity = db.Column(db.Integer)

    def __init__(self, room, building, campus, capacity):
        self.room = room
        self.building = building
        self.campus = campus
        self.capacity = capacity

