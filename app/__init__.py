# Import flask and template operators
from flask import Flask, render_template, send_from_directory, url_for

# Define the WSGI application object
app = Flask(__name__, template_folder='templates')

# Configurations
app.config.from_object('config')

from app.mod_db import *

# Define the database object which is imported
# by modules and controllers

# login_manager = LoginManager()

@app.route('/')
def home_index():
    join_cond = (Rooms.room_number == Counts.counts_room_number)
    building = Rooms.select(Rooms, Counts).join(Counts, on=join_cond).where((Rooms.room_number=="B002") & (Counts.counts_time ** "%Nov 02%")).naive()
    print(building.sql())
    for item in building:
        print(item.counts_time)
    return render_template("login.html")

# development use
@app.route('/static/<path:path>')
def send_static(path):
    print(path)
    return send_from_directory(url_for("static"), path)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_hello)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_api.controllers import mod_api as api_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(api_module)

