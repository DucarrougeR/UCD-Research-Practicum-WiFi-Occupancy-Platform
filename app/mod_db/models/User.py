# Luke Kearney
from werkzeug.security import generate_password_hash, check_password_hash
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
        if User.create(email=email, password=generate_password_hash(password), group=group):
            return True
        return False

    @staticmethod
    def authenticate_user(email, password):

        user = User.select(User).where((User.email == email))
        if user.count():
            user = user.get()
            if check_password_hash(user.password, password):
                return user

        return None

    @staticmethod
    def cleaned(user):
        if user['password']:
            del user['password']

        if user['id']:
            del user['id']
        return user


User.create_table(fail_silently=True)
# user = User.authenticate_user("admin@admin.com", "password")
# print(user)