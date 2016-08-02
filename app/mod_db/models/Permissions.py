# Luke Kearney
from peewee import *
from .BaseModel import BaseModel
import json


class Permissions(BaseModel):
    user_group = CharField(primary_key=True)
    rules = CharField(unique=True, null=False)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)


    @staticmethod
    def get_permission_for_user_group(group_id):
        permission_set = Permissions.select(Permissions).where(Permissions.user_group == group_id).get()
        if permission_set:
            return permission_set
        return None


Permissions.create_table(fail_silently=True)
# user = User.authenticate_user("admin@admin.com", "password")
# print(user)