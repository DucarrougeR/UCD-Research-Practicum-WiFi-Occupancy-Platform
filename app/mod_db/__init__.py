from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

from .models import *
