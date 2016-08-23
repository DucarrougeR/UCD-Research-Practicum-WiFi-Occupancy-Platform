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
from app.values import mail_config

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


                        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
                        # return redirect(url_for('uploaded_file',
                        #                         filename=filename))
                        resp = api_upload_file(file.filename, filetype)
                        if "error" in resp.keys():
                            return jsonify(resp), 500

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

        if "email" not in data.keys() or "password" not in data.keys():
            return jsonify({"error": strings.ERROR_LOGIN}), 403

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
            return jsonify({"error": strings.ERROR_LOGIN}), 403

@mod_api.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = json.loads(request.data.decode())
        if "email" not in data.keys():
            return jsonify({"error": strings.ERROR_REGISTER_USER}), 500

        email = data['email']
        password = User.generate_password()
        if "permission" in data.keys():
            permission = data['permission']
        else:
            permission = Permissions.default_permission
        if Permissions.user_has_permission(current_user, 'add-user'):
            if User.create_new(email, password, permission):
                # notify the new user


                msg = Message(strings.EMAIL_HEADING_REGISTER,
                              sender="wispyapp@gmail.com",
                              recipients=[email])
                msg.html = gen_email(email, password)
                mail.send(msg)


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
    modules = Classes.select(Classes.classes_module_code).distinct() \
        .order_by(Classes.classes_module_code.asc())
    module_list = []
    for module in modules:
        print(module)
        result = module.get_result()

        regex = re.match("(.+) & (.+)", result["classes_module_code"])
        regex2 = re.match("(.+) \(.+\)", result["classes_module_code"])

        # if 2 modules listed in 1
        if regex:

            code = regex.groups()[0]
            module_list.append(code)
            code = regex.groups()[1]
            module_list.append(code)
        elif regex2:
            # has lecture and practicals
            code = regex2.groups()[0]
            module_list.append(code)
        else:
            module_list.append(result["classes_module_code"])

    return jsonify(list(set(module_list)))

@mod_api.route('/module/rooms-used/<module>', methods=['GET'])
def get_module_info(module):
    query = "%" + module + "%"
    results = Classes.select(Classes).distinct(Classes.classes_room_number)\
        .where(Classes.classes_module_code ** query)

    result_list = []
    times = []
    for result in results:
        print(result)
        result = result.get_result()
        regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2}):.", result["classes_time"])
        groups = regex.groups()
        day_time = groups[0] + " " + groups[1]
        if day_time not in times:

            #regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["classes_time"])

            time = {
                "day": groups[0],
                "hour": groups[1]
            }

            result["classes_time"] = time
            times.append(day_time)
            result_list.append(result)

    return jsonify({"results": result_list})

@mod_api.route('/module/room/<room>', methods=['GET'])
def get_module_info_by_room(room):

    results = Classes.select(Classes.classes_time, Classes.classes_module_code, Classes.classes_room_number)\
        .where((Classes.classes_room_number == room) & (Classes.classes_module_code != None))

    result_list = []
    times = []
    for result in results:

        result = result.get_result()

        # Mon
        # Nov
        # 02
        # 20:00:00
        regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2}):.", result["classes_time"])
        groups = regex.groups()
        day_time = groups[0] + " " + groups[1]

        if re.match("[A-Za-z]+\d+.*", result["classes_module_code"]):
            if day_time not in times:

                #regex = re.match("([A-Za-z)]{3}) [A-Za-z]{3} \d{2} (\d{2})", result["classes_time"])

                time = {
                    "day": groups[0],
                    "hour": groups[1]
                }

                result["classes_time"] = time
                times.append(day_time)
                result_list.append(result)

    print(len(result_list))
    return jsonify({"results": result_list})

@mod_api.route('/rooms/usage/most', methods=['GET'])
def get_most_used_rooms():
    # fetches rooms which have the most classes
    # SELECT COUNT(classes_room_number), classes_room_number FROM classes  WHERE classes_module_code IS NOT null GROUP BY classes_room_number
    #results = Classes.select(Classes.classes_room_number).group_by(Classes.classes_room_number).count()
    results = db.execute_sql('SELECT COUNT(classes_room_number) as cnt, classes_room_number FROM classes WHERE classes_module_code IS NOT null GROUP BY classes_room_number ORDER BY cnt DESC LIMIT 5')
    results = results.fetchall()
    result_list = []
    for result in results:
        result_dict = {"room": result[1],
                       "count": result[0]}
        result_list.append(result_dict)
    return jsonify(result_list)

@mod_api.route('/rooms/usage/least', methods=['GET'])
def get_least_used_rooms():
    results = db.execute_sql(
        'SELECT COUNT(classes_room_number) as cnt, classes_room_number FROM classes WHERE classes_module_code IS NOT null GROUP BY classes_room_number ORDER BY cnt ASC LIMIT 5')
    results = results.fetchall()
    result_list = []
    for result in results:
        result_dict = {"room": result[1],
                       "count": result[0]}
        result_list.append(result_dict)
    return jsonify(result_list)

