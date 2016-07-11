from app.mod_db import db

class Data(db.Model):
    __tablename__ = 'class'
    room = db.Column(db.String(5), primary_key=True)
    time = db.Column(db.String(100), primary_key=True)
    associated = db.Column(db.Integer)
    authenticated = db.Column(db.Integer)
    occupancy = db.Column(db.String(100))
    occupancyCount = db.Column(db.Integer)

    def __init__(self, room, time, associated, authenticated, occupancy, occupancy_count):
        self.room = room
        self.time = time
        self.associated = associated
        self.authenticated = authenticated
        self.occupancy = occupancy
        self.occupancyCount = occupancy_count
