from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username











# CONNECTION
conn = sqlite3.connect("TimeTable.db") # Connect to database (creates if it does not exist)
cursor = conn.cursor()

# Create a new table in the current database
# Specify column names and data types
cursor.execute("CREATE TABLE IF NOT EXISTS TimeTable (class_room  String(10), time DateTime, date Integer, week_day Text, month Text, year Integer, associated Integer, authenticated Integer, full Boolean)")
conn.commit() # Save the changes

# INSERTION
# source: http://flask.pocoo.org/snippets/37/
def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    return id



# Handling multiple sub-requests in a single Flask request
# http://flask.pocoo.org/snippets/131/