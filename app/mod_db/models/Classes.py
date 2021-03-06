# from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel
# class Classes(db.Model):
#     __tablename__ = 'classes'
#     room = db.Column(db.String(5), primary_key=True)
#     time = db.Column(db.String(100))
#     module = db.Column(db.String(100))
#     size = db.Column(db.Integer)
#
#     def __init__(self, room, time, module, size):
#         self.room = room
#         self.time = time
#         self.module = module
#         self.size = size

class Classes(BaseModel):
    classes_module_code = CharField(null=False)
    classes_size = CharField(null=False)
    classes_room_number = CharField(null=False)
    classes_time = CharField(null=False)
    classes_attendance_score = FloatField(null=False)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)


    class Meta:
        primary_key = CompositeKey('classes_room_number', 'classes_time')

