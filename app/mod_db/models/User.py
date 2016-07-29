# Luke Kearney
from werkzeug.security import generate_password_hash, check_password_hash
from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel
from flask_peewee.auth import Auth
from flask_peewee.db import Database

class User(BaseModel):
    password = CharField()
    email = CharField()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def create_new(self, email, password):
        User.create(email=email, password=generate_password_hash(password))

    def authenticate_user(self, email, password):
        user = User.select(User).where((User.email == email) & (User.password ** generate_password_hash(password))).get()
        return user
