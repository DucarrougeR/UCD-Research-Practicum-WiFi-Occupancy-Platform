from flask_sqlalchemy import SQLAlchemy
from app import app
from peewee import *
import config
# creates a SQLAlchemy instance using the app config (see app/__init__.py)
#db = SQLAlchemy(app)

db = SqliteDatabase(config.DATABASE)

# imports the models
from .models import *


db.connect()

# creates tables if they don't exist
db.create_tables([User], safe=True)
# db.create_all()

# db.session.commit()
