class Logs(db.Model):
    __tablename__ = 'Logs'
    campus = db.Column(db.String(20))
    building = db.Column(db.String(20), primary_key=True)
    room = db.Column(db.String(10), primary_key=True, db.ForeignKey)
    date = db.Column(db.DateTime)
    associated = db.Column(db.Integer)
    authenticated = db.Column(db.Integer)

    def __init__(self, campus, building, room, date, associated, authenticated):
        self.campus = campus
        self.building = building
        self.room = room
        self.date = date
        self.associated = associated
        self.authenticated = authenticated

    def __repr__(self):
        return '<User %r>' % self.room




#http://flask-sqlalchemy.pocoo.org/2.1/models/
