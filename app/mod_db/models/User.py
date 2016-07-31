# Luke Kearney
from werkzeug.security import generate_password_hash, check_password_hash
from app.mod_db import db
from peewee import *
from .BaseModel import BaseModel


class User(BaseModel):
    password = CharField(null=False)
    email = CharField(unique=True, null=False)
    group = CharField()

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def create_new(email, password, group="user"):
        User.create(email=email, password=generate_password_hash(password), group=group)

    @staticmethod
    def authenticate_user(email, password):
        user = User.select(User).where((User.email == email)).get()
        if check_password_hash(user.password, password):
            return user
        return None

User.create_table(fail_silently=True)
# user = User.authenticate_user("admin@admin.com", "password")
# print(user)