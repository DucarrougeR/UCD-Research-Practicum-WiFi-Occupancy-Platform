from app import app
from peewee import *
import config
# creates a SQLAlchemy instance using the app config (see app/__init__.py)
from app import app, DATABASE
from flask_peewee.auth import Auth
from flask_peewee.db import Database

print(DATABASE)
db = SqliteDatabase(DATABASE["name"])
auth_db = Database(app)
# imports the models
from .models import *


db.connect()

# creates tables if they don't exist
#db.create_tables([], safe=True)
# db.create_all()

# db.session.commit()
