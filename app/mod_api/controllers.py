# Luke Kearney
# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app.app_forms.forms import SignupForm, LoginForm
# from flask_login import login_user, logout_user, LoginManager, login_required, user_logged_out, user_logged_in
from app import db, app
from app.mod_db import *
import re
from .models import *
import os
from werkzeug.utils import secure_filename


mod_api = Blueprint('mod_api', __name__, url_prefix='/api')

# login_manager.init_app(app)
# login_manager.login_view = 'mod_auth.login'

# Set the route and accepted methods
@mod_api.route('/hello', methods=['GET', 'POST'])
def hello():
    return jsonify("hello")

@mod_api.route('/room/occupancy/<room>/')
@mod_api.route('/room/occupancy/<room>/<time>')
def occupancy_data(room, time=None):
    if time:
        time = " ".join(time.split("%20"))

        dateRe = re.compile("([A-Za-z]{3}) ([A-Za-z]{3}) (\d{2}) (\d{4})")
        if (is_valid_date(time)):

            date = parse_date(time)

            # print("%"+ " ".join((date[0], date[1], date[2])) +"%")
            join_cond = (Rooms.room_number == Counts.counts_room_number)
            date_cond = "%" + date[1] + " " + date[2] + "%"
            results = Rooms.select(Rooms, Counts).join(Counts, on=join_cond).where(
                (Rooms.room_number == room) & (Counts.counts_time ** date_cond)).naive()
    else:
        join_cond = (Rooms.room_number == Counts.counts_room_number)
        results = Rooms.select(Rooms, Counts).join(Counts, on=join_cond).where(
            (Rooms.room_number == room)).naive()


    results_list = []

    for result in results:
        # gets the fields of the result set
        fields = Counts._meta.sorted_field_names + Rooms._meta.sorted_field_names
        results_dict = {}

        for field in fields:
            # creates a dictionary of each result
            results_dict[field] = getattr(result, field)
        results_list.append(results_dict)

    return jsonify({"results" : results_list})

@mod_api.route('/data/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            return "uploaded"
