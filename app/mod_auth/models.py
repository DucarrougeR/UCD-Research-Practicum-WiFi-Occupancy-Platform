# # Luke Kearney
from peewee import *
from flask_peewee.auth import *
from werkzeug.security import generate_password_hash, check_password_hash
from app.mod_db.models import User
from flask_peewee.auth import BaseUser
from app import auth_db

class User():
    username = CharField()
    #     password = CharField()
    #     email = CharField()
    #
    #     # ... our custom fields ...
    #     is_superuser = BooleanField()

# class User(auth_db.Model, BaseUser):
#


