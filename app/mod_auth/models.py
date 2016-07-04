# Luke Kearney
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, email, password_plain):
        self.email = email.lower()
        self.set_password(password_plain)

    def set_password(self, password_plain):
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        print password_plain
        print self.password
        return check_password_hash(self.password, password_plain)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print self.id
        return unicode(self.id)


class Email:
    def is_valid_extension(self, email):
        return True