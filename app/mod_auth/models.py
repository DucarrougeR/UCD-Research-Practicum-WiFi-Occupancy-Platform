# # Luke Kearney
from peewee import *
from flask_peewee.auth import *
from werkzeug.security import generate_password_hash, check_password_hash

from flask_peewee.auth import BaseUser
from app import auth_db


# class User(auth_db.Model, BaseUser):
#


