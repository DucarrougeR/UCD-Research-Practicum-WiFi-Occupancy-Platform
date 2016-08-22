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

    room_number = CharField(null=False, primary_key=True)
    room_building = CharField(null=False)
    room_campus = CharField(null=False)
    room_capacity = IntegerField(null=False)
    room_occupancy_score = FloatField(null=False)
    room_rssi_baseline = FloatField(null=False)
    room_audio_baseline = FloatField(null=False)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        # self.rooms_rooms_number = room
        # self.rooms_build = building
        # self.rooms_campus = campus
        # self.rooms_capacity = capacity

