from app.mod_db import db

class Classes(db.Model):
    __tablename__ = 'classes'
    room = db.Column(db.String(5), primary_key=True)
    time = db.Column(db.String(100))
    module = db.Column(db.String(100))
    size = db.Column(db.Integer)

    def __init__(self, room, time, module, size):
        self.room = room
        self.time = time
        self.module = module
        self.size = size
