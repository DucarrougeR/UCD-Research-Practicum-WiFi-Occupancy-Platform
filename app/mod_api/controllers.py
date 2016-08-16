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
import json
from flask_mail import Message
from app import mail
from app.mod_stat import *
import sqlite3
from app.values import strings
from app.mod_db import data_clean

mod_api = Blueprint('mod_api', __name__, url_prefix='/api')

# Set the route and accepted methods
@mod_api.route('/hello', methods=['GET', 'POST'])
def hello():
    return jsonify("hello")

@mod_api.route('/module/<module>')
def module_data(module):
    return jsonify(get_module_results(module))


@mod_api.route('/room/occupancy/<room>/')
@mod_api.route('/room/occupancy/<room>/<time>/<type>')
def occupancy_data(room, time=None, type=None):
    results = None
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
            # results = Counts.select(Counts).where((Counts.counts_room_number == room)
    else:
        join_cond = (Rooms.room_number == Counts.counts_room_number)
        results = Rooms.select(Rooms, Counts).join(Counts, on=join_cond).where(
            (Rooms.room_number == room)).naive()

    print(results)
    results_list = []
    if results:
        for result in results:
            # gets the fields of the result set
            # fields = Counts._meta.sorted_field_names + Rooms._meta.sorted_field_names
            fields = ["counts_room_number", "counts_time", "counts_module_code",
                      "counts_predicted", "counts_predicted_is_occupied", "room_capacity", "room_occupancy_score"]
            results_dict = {}

            for field in fields:
                # creates a dictionary of each result
                results_dict[field] = getattr(result, field)
                # print(results_dict)
                if type == "binary":
                    # if binary data, transform to 1 or 0
                    pass
            results_list.append(results_dict)





    return jsonify({"results" : results_list})

@mod_api.route('/data/upload/<filetype>', methods=['POST'])
def upload_file(filetype):
    # check if user is logged in and has permission to use the route
    if current_user.is_authenticated:
        if request.method == 'POST':
            # check if the filetype was defined
            print(request.data.decode())
            # #data = json.loads(request.data.decode())
            if filetype and (filetype == "wifi" or filetype == "truth" or filetype == "timetable"):
                if Permissions.permissions_for_filetype(current_user, filetype):
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
                            print(file.filename)
                            df = predict.predict(file.filename)

                            # Writes dataframe with predictions to database.
                            df.columns = ["counts_room_number", "counts_time", "counts_associated", "counts_authenticated", "counts_predicted", "counts_predicted_is_occupied"]
                            con = sqlite3.connect(config.DATABASE["name"])
                            df.to_sql("counts", con, flavor="sqlite", if_exists="append", index=False, chunksize=None)
                        # Else new file is a .zip filled with CSVs.
                        elif file.filename.endswith(".zip"):
                            # Unzips all of the zips.
                            data_clean.unzip(app.config["UPLOAD_FOLDER"])

                            # Loops through every CSV file in every folder in the directory.
                            for root, dirs, files in os.walk(app.config["UPLOAD_FOLDER"]):
                                for f in files:
                                    # Generates predictions for the file.
                                    df = predict.predict(f)
                                    if df:
                                        # Writes dataframe with predictions to database.
                                        df.columns = ["counts_room_number", "counts_time", "counts_associated", "counts_authenticated", "counts_predicted", "counts_predicted_is_occupied"]
                                        con = sqlite3.connect(config.DATABASE["name"])
                                        df.to_sql("counts", con, flavor="sqlite", if_exists="append", index=False, chunksize=None)
                                    else:
                                        return jsonify({"error": strings.ERROR_BAD_FILE}), 500
                        return jsonify({"success": strings.SUCCESS_FILE_UPLOAD})

                else:
                    return jsonify({"error": strings.ERROR_NO_PERMISSION}), 403
    else:
        return jsonify({"error": strings.ERROR_NOT_LOGGED_IN})

@mod_api.route('/auth/login', methods=['POST'])
def log_in_user():
    if request.method == 'POST':
        # convert from JSON string to python
        data = json.loads(request.data.decode())
        email = data['email']
        password = data['password']

        # check if the user is valid
        user = User.authenticate_user(email, password)
        if user:
            # log the user in using flask_login
            login_user(user)
            # convert the user object to standard, serializable, python
            user = user.get_result()
            permissions = Permissions.get_permission_for_user_group(user["group"]).get_result()
            # converts string of permissions to standard python object
            user["permissions"] = json.loads(permissions["rules"])

            return jsonify(User.cleaned(user))
        else:
            return jsonify({"error": strings.ERROR_LOGIN}), 404

@mod_api.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = json.loads(request.data.decode())
        email = data['email']
        password = User.generate_password()
        if data['permission']:
            permission = data['permission']
        else:
            permission = Permissions.default_permission
        if Permissions.user_has_permission(current_user, 'add-user'):
            if User.create_new(email, password, permission):
                # notify the new user
                try:
                    msg = Message("Hello",
                                  sender=config.DEFAULT_MAIL_SENDER,
                                  recipients=[email])
                    msg.html = "<h1>Hello, you've been signed up for our app</h1>Your password is: " + password
                    mail.send(msg)
                except Exception:
                    print("error sending email")

                return jsonify({"success": strings.SUCCESS_REGISTER_USER}), 200
            else:
                return jsonify({"error": strings.ERROR_REGISTER_USER}), 500
        else:
            return "Page not found", 404


@mod_api.route('/auth/loggedin', methods=['GET'])
def logged_in_user():
    if current_user.is_authenticated:
        return jsonify({"loggedIn": True})
    else:
        return jsonify({"loggedIn": False})

@mod_api.route('/auth/current-user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        user = current_user.get_result()
        permissions = Permissions.get_permission_for_user_group(user["group"]).get_result()
        # converts string of permissions to standard python object
        user = User.cleaned(user)
        user["permissions"] = json.loads(permissions["rules"])
        return jsonify(user)
    else:
        return jsonify(None)

@mod_api.route('/auth/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"success": strings.SUCCESS_LOGOUT})
    else:
        return jsonify({"error": strings.ERROR_LOGOUT}), 500


@mod_api.route('/auth/permissions/get-all', methods=['GET'])
def get_all_permissions():
    # TODO: only allow adding of permissions at same or lower level than current user's permission level (may require some kind of hierarchy integer)
    return jsonify(Permissions.get_all())

@mod_api.route('/rooms/list', methods=['GET'])
def get_rooms():
    rooms = Rooms.select(Rooms.room_number)
    rooms_list = []
    for room in rooms:
        rooms_list.append(room.get_result())

    return jsonify(rooms_list)

@mod_api.route('/module/list', methods=['GET'])
def get_modules():
    modules = Allocation_Score.select(Allocation_Score.counts_module_code).distinct() \
        .order_by(Allocation_Score.counts_module_code.asc())
    module_list = []
    for module in modules:
        result = module.get_result()
        regex = re.match("(.+) & (.+)", result["counts_module_code"])
        regex2 = re.match("(.+) \(.+\)", result["counts_module_code"])

        # if 2 modules listed in 1
        if regex:
            res = result
            code = regex.groups()[0]
            module_list.append(code)
            code = regex.groups()[1]
            module_list.append(code)
        elif regex2:
            # has lecture and practicals
            code = regex2.groups()[0]
            module_list.append(code)
        else:
            module_list.append(result["counts_module_code"])

    return jsonify(list(set(module_list)))

@mod_api.route('/module/rooms-used/<module>', methods=['GET'])
def get_module_info(module):
    query = "%" + module + "%"
    results = Allocation_Score.select(Allocation_Score).distinct(Allocation_Score.counts_room)\
        .where(Allocation_Score.counts_module_code ** query)

    result_list = []
    times = []
    for result in results:

        result = result.get_result()
        regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["counts_time"])
        groups = regex.groups()
        day_time = groups[0] + " " + groups[1]
        if day_time not in times:

            regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["counts_time"])

            time = {
                "day": groups[0],
                "hour": groups[1]
            }

            result["counts_time"] = time
            times.append(day_time)
            result_list.append(result)

    return jsonify({"results": result_list})

@mod_api.route('/module/room/<room>', methods=['GET'])
def get_module_info_by_room(room):

    results = Allocation_Score.select(Allocation_Score.counts_time, Allocation_Score.counts_module_code, Allocation_Score.counts_room)\
        .where(Allocation_Score.counts_room == room)

    result_list = []
    times = []
    for result in results:

        result = result.get_result()
        regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["counts_time"])
        groups = regex.groups()
        day_time = groups[0] + " " + groups[1]
        if day_time not in times:

            regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["counts_time"])

            time = {
                "day": groups[0],
                "hour": groups[1]
            }

            result["counts_time"] = time
            times.append(day_time)
            result_list.append(result)

    print(result_list)
    return jsonify({"results": result_list})

