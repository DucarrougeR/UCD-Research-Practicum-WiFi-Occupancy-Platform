#Romain Ducarrouge
from flask import Flask 

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


'''sources
engine creation: http://docs.sqlalchemy.org/en/latest/core/engines.html
video for SQLAlchemy https://www.youtube.com/watch?v=f_-ApViOv20
'''