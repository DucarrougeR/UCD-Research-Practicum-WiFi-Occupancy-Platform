# Luke Kearney
from werkzeug.security import generate_password_hash, check_password_hash
from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel

class User(BaseModel):
    id = IntegerField(primary_key=True, null=True)
    email = CharField()
    password = CharField()


    def __init__(self, email, password_plain):
        super(BaseModel,self).__init__()

        self.email = email.lower()
        self.set_password(password_plain)
        self.save()

    def set_password(self, password_plain):
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        print(password_plain)
        print(self.password)
        return check_password_hash(self.password, password_plain)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print(self.id)
        return self.id