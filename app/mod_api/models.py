# Luke Kearney
import re
import config
from app.mod_db.models import *
from app.values import strings
from app.mod_stat import predict
from app.mod_db import data_clean
import sqlite3
import app
import pandas as pd
import os


def parse_date(date):
    date_re = re.compile("([A-Za-z]{3}) ([A-Za-z]{3}) (\d{2}) (\d{4})")
    grouped_dates = date_re.match(date).groups()
    valid_months = ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    valid_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    if grouped_dates[0] not in valid_days:
        return False

    if grouped_dates[1] not in valid_months:
        return False

    if int(grouped_dates[2]) > 31:
        return False

    if int(grouped_dates[3]) <= 0:
        return False

    return grouped_dates


def is_valid_date(date):
    date_re = re.compile("([A-Za-z]{3}) ([A-Za-z]{3}) (\d{2}) (\d{4})")

    if not date_re.match(date):
        return False

    grouped_dates = date_re.match(date).groups()
    valid_months = ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    valid_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    if grouped_dates[0] not in valid_days:
        return False

    if grouped_dates[1] not in valid_months:
        return False

    if int(grouped_dates[2]) > 31:
        return False

    if int(grouped_dates[3]) <= 0:
        return False

    return True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


def get_module_results(module):
    # get the attendance information for a module on each day
    results = Classes.select(Classes).where(Classes.classes_module_code == module)

    # display on graph showing day and time (bar chart?). For attendance show it as average for all times that day occurs

    results_by_day = {}
    rooms_dict = {}
    for result in results:
        result_dict = result.get_result()

        # check for room data if its not already there
        if result_dict["classes_room_number"] not in rooms_dict:
            rooms_dict[result_dict["classes_room_number"]] = \
                Rooms.select(Rooms.room_capacity).where(
                    Rooms.room_number == result_dict["classes_room_number"]).get().get_result()

        # add the room capacity
        result_dict["room_capacity"] = rooms_dict[result_dict["classes_room_number"]]

        regex = re.match("([A-Za-z]{3}) ([A-Za-z]{3}) (\d{2}) (\d{2})", result_dict["classes_time"])
        groups = regex.groups()

        # note this doesn't take years and semesters into account
        # appends the class if the day is already listed. Creates a new list if its not
        if groups[0] in results_by_day:
            if groups[3] in results_by_day[groups[0]]:
                results_by_day[groups[0]][groups[3]].append(result_dict)
            else:
                results_by_day[groups[0]][groups[3]] = [result_dict]
        else:
            results_by_day[groups[0]] = {
                groups[3]: [result_dict]
            }

        # add the attendance percent for that date and time
        # get the capacities at this day and time
        regexp = groups[0] + " [A-Za-z]{3} (\d{2}) " + groups[3]

        counts_results = Counts.select(Counts.counts_module_code, Counts.counts_predicted_is_occupied,
                                       Counts.counts_time, Counts.counts_predicted) \
            .where(Counts.counts_time.regexp(regexp) == True)

        average = 0
        minimum = 1000
        maximum = 0

        for result in counts_results:

            result_dict = result.get_result()

            if result_dict["counts_predicted"] is not None:
                try:

                    average = (average + int(result_dict["counts_predicted"])) / 2
                    maximum = max(maximum, int(result_dict["counts_predicted"]))
                    minimum = min(minimum, int(result_dict["counts_predicted"]))
                except Exception:
                    print("Exception")
                    print(result_dict)

        return {"day": results_by_day, "rooms_used": rooms_dict}


def api_upload_file(filename, filetype):
    # If new file is a single CSV:
    if filename.endswith(".csv"):
        # Generates predictions for the file.
        if filetype == "wifi":
            df = predict.predict(filename)

            # Writes dataframe with predictions to database.
            df.columns = ["counts_room_number", "counts_time", "counts_associated", "counts_authenticated",
                          "counts_predicted", "counts_predicted_is_occupied"]
            con = sqlite3.connect(config.DATABASE["name"])
            df.to_sql("counts", con, flavor="sqlite", if_exists="append", index=False, chunksize=None)
        elif filetype == "timetable":
            df = pd.read_csv(os.path.join(config.UPLOAD_FOLDER, filename))

            for index, row in df.iterrows():
                if row["room"] == "None":
                    row["room"] = None
                if row["module"] == "None":
                    row["module"] = None
                if row["time"] == "None":
                    row["time"] = None
                if row["size"] == "None":
                    row["size"] = None

                row["room"] = row["room"].replace(".", "")

                try:
                    classes = Classes.select(Classes).where((Classes.classes_room_number == row["room"]) &
                                                            (Classes.classes_time == row["time"])).get()
                except Exception:
                    classes = None

                if classes:
                    # update the row
                    classes.classes_size = row["size"]
                    classes.classes_module_code = row["module"]
                    classes.save()
                else:
                    # insert new new row
                    Classes.create(classes_module_code=row["module"], classes_time=row["time"],
                                   classes_room_number=row["room"], classes_size=row["size"])
        elif filetype == "truth":
            df = pd.read_csv(os.path.join(config.UPLOAD_FOLDER, filename))
            for index, row in df.iterrows():
                if row["room"] == "None":
                    row["room"] = None
                if row["capacity"] == "None":
                    row["capacity"] = None
                if row["time"] == "None":
                    row["time"] = None
                if row["occupancy"] == "None":
                    row["occupancy"] = None

                try:
                    # Mon Nov 02 09:00:00
                    groups = re.match("[A-Za-z]{3} [A-Za-z]{3} \d{2} (\d{2}).+").groups()
                    time = "%" + groups[0] + "%"
                    counts = Counts.select(Counts).where((Counts.counts_time ** time) &
                                                         (Counts.counts_room_number == row["room"]))
                except Exception:
                    classes = None

                percent = int(row["occupancy"][:-1]) / 100
                if classes:
                    # update the row

                    for count in counts:
                        count.counts_truth_percent = row["occupancy"]
                        count.counts_truth = int(row["capacity"] * percent)
                        if percent > 1:
                            count.counts_truth_is_occupied = 1
                        else:
                            count.counts_truth_is_occupied = 0
                        count.save()
                else:
                    # insert new new row
                    if percent > 1:
                        is_occupied = 1
                    else:
                        is_occupied = 0
                    Counts.create(counts_room_number=row["room"], counts_truth_percent=row["occupancy"],
                                  counts_truth=int(row["capacity"] * percent), counts_truth_is_occupied=is_occupied,
                                  counts_time=row["time"])

    # Else new file is a .zip filled with CSVs.
    elif filename.endswith(".zip"):  # Unzips all of the zips.
        data_clean.unzip(filename)

        # Loops through every CSV file in every folder in the directory.
        for root, dirs, files in os.walk(filename):
            for f in files:
                if f.endswith(".csv"):
                    # Generates predictions for the file.
                    resp = api_upload_file(f, filetype)
                    if "error" in resp.keys():
                        return {"error": strings.ERROR_BAD_FILE}
                    api_upload_file(filename, filetype)
                else:
                    return {"error": strings.ERROR_BAD_FILE}

    return {"success": strings.SUCCESS_FILE_UPLOAD}

def gen_email(email, password):
    string = "<p>Hello, you've been registered for the WiSpy platform. Your login credentials are: <br> Email:" + email + \
             "<br>Password: " + password
    return string
