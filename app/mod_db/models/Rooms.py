# Luke Kearney
from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel

# class Building(BaseModel):
#     __tablename__ = 'building'
#     room = db.Column(db.String(5), primary_key=True)
#     building = db.Column(db.String(100))
#     campus = db.Column(db.String(100))
#     capacity = db.Column(db.Integer)
#
#     def __init__(self, room, building, campus, capacity):
#         self.room = room
#         self.building = building
#         self.campus = campus
#         self.capacity = capacity

class Rooms(BaseModel):

    rooms_rooms_number = CharField(null=False, primary_key=True)
    rooms_build = CharField(null=False)
    rooms_campus = CharField(null=False)
    rooms_capacity = IntegerField()

    def __init__(self, room, building, campus, capacity):
        super(BaseModel, self).__init__()
        self.rooms_rooms_number = room
        self.rooms_build = building
        self.rooms_campus = campus
        self.rooms_capacity = capacity

