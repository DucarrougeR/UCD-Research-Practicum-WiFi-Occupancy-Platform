from flask_sqlalchemy import SQLAlchemy
from app import app

# creates a SQLAlchemy instance using the app config (see app/__init__.py)
db = SQLAlchemy(app)

# imports the models
from .models import *

# creates tables if they don't exist
db.create_all()
db.session.commit()
