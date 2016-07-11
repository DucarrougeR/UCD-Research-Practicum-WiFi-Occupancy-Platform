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
    classes_module_code = CharField(null=False, primary_key=True)
    classes_size = CharField(null=False)
    classes_room_number = CharField(null=False)
    classes_time = IntegerField(primary_key=True)

    def __init__(self, room, time, module, size):
        super(BaseModel, self).__init__()
        self.classes_room_number = room
        self.classes_time = time
        self.classes_module_code = module
        self.classes_size = size

