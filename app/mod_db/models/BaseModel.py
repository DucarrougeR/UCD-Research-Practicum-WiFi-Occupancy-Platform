from app.mod_db import db
from peewee import *

class BaseModel(Model):
    class Meta:
        database = db