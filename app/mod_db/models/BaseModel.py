from app.mod_db import db
from peewee import *
import json

class BaseModel(Model):
    # http://stackoverflow.com/questions/21975920/peewee-model-to-json
    def __str__(self):
        r = {}
        for k in self._data.keys():
            print(k)
            # try:
            #     r[k] = str(getattr(self, k))
            # except:
            #     r[k] = json.dumps(getattr(self, k))
        return "hllo"

    class Meta:
        database = db