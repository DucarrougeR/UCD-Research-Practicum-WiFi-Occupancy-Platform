# from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel


class Allocation_Score(BaseModel):
    counts_date = IntegerField(null=False)
    counts_hour = IntegerField(null=False)
    counts_room = CharField(null=False)
    counts_time = CharField(null=False)
    counts_capacity = IntegerField(null=False)
    counts_truth_percent = CharField(null=False)
    counts_truth = IntegerField(null=False)
    counts_module_code = CharField(null=False)
    counts_size = IntegerField(null=False)
    counts_associated = IntegerField(null=False)
    counts_authenticated = IntegerField(null=False)
    room_allocation_score = IntegerField(null=False)


    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)


