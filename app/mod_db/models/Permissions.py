# Luke Kearney
from peewee import *
from .BaseModel import BaseModel
import json


class Permissions(BaseModel):
    user_group = CharField(primary_key=True)
    rules = CharField(unique=True, null=False)

    default_permission = "user"

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)


    @staticmethod
    def get_permission_for_user_group(group_id):
        permission_set = Permissions.select(Permissions).where(Permissions.user_group == group_id).get()
        if permission_set:
            return permission_set
        return None

    @staticmethod
    def get_all():
        permission_set = Permissions.select(Permissions)
        permissions = []
        for permission in permission_set:
            permissions.append(permission.get_result()["user_group"])
        print(permissions)
        return permissions

    @staticmethod
    def user_has_permission(user, permission):
        permissions = Permissions.get_permission_for_user_group(user.group)
        rules = json.loads(permissions.rules)
        if rules[permission]:
            return True
        return False



Permissions.create_table(fail_silently=True)
# user = User.authenticate_user("admin@admin.com", "password")
# print(user)