import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
	 
# Create the application
app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('COMP47350', silent=True)

def connect_db():
    # Connects to database
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    # Opens database connection 
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    # Closes the database after request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
	
def init_db():
	db = get_db()
	with app.open_resource("schema.sql", more='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	# initialize database
	init_db()
	print ("Database initialized")


	
if __name__ == '__main__':
    #init_db()
    app.run()
	
	
	
	
	
'''sources
engine creation: http://docs.sqlalchemy.org/en/latest/core/engines.html
video for SQLAlchemy https://www.youtube.com/watch?v=f_-ApViOv20
GitHub repo for Flaskr tutorial to flask and sql
'''	