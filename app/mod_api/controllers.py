# Luke Kearney
# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app.app_forms.forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, LoginManager, login_required, user_logged_out, user_logged_in
from app import db, login_manager, app
from app.mod_db import *


mod_api = Blueprint('mod_api', __name__, url_prefix='/api')

login_manager.init_app(app)
login_manager.login_view = 'mod_auth.login'

# Set the route and accepted methods
@mod_api.route('/hello', methods=['GET', 'POST'])
def hello():
    return jsonify("hello")

@mod_api.route('/room/occupancy/<room>/')
@mod_api.route('/room/occupancy/<room>/<time>')
def occupancy_data(room, time=None):
    data = Counts.select().where(Counts.counts_room_number == room)
    print(len(data))
    # for d in data:
    #     print(d)

    return jsonify("hello")
