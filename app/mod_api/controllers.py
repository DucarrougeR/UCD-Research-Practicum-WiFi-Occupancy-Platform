# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app.mod_db import *
from .models import *
import os
from werkzeug.utils import secure_filename
from app.mod_db.models import User
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app.values import strings
import sqlite3

mod_api = Blueprint('mod_api', __name__, url_prefix='/api')

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

            # If new file is a single CSV:
            if file.filename.endswith(".csv"):
                # Generates predictions for the file. 
                df = mod_stat.predict.predict(file)

                # Writes dataframe with predictions to database. 
                df.columns = ["room", "counts_time", "counts_associated", "counts_authenticated", "counts_predicted"]
                con = sqlite3.connect(config.DATABASE["name"])    
                df.to_sql("counts", con, flavor="sqlite", if_exists="replace", index=False, chunksize=None)
            # Else new file is a .zip filled with CSVs. 
            elif file.filename.endswith(".zip"):
                # Unzips all of the zips. 
                mod_db.data_clean(app.config["UPLOAD_FOLDER"])

                # Loops through every CSV file in every folder in the directory.
                for root, dirs, files in os.walk(app.config["UPLOAD_FOLDER"]):
                    for f in files:
                        # Generates predictions for the file. 
                        df = mod_stat.predict.predict(f)

                        # Writes dataframe with predictions to database. 
                        df.columns = ["room", "counts_time", "counts_associated", "counts_authenticated", "counts_predicted"]
                        con = sqlite3.connect(config.DATABASE["name"])    
                        df.to_sql("counts", con, flavor="sqlite", if_exists="replace", index=False, chunksize=None)

            return "uploaded"

@mod_api.route('/auth.login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.authenticate_user(email, password)
        if user:
            login_user(user)
            return jsonify(user)
        else:
            return jsonify({"error": strings.ERROR_LOGIN})

@mod_api.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.create_new(email, password):
            return jsonify({"success": strings.SUCCESS_REGISTER_USER})
        else:
            return jsonify({"error": strings.ERROR_REGISTER_USER})


@mod_api.route('/auth/loggedin', methods=['GET'])
def logged_in_user():
    if current_user.is_authenticated:
        return jsonify({"loggedIn": True})
    else:
        return jsonify({"loggedIn": False})
