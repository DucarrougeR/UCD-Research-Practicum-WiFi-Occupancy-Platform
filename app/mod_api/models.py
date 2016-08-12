# Luke Kearney
import re
import config
from app.mod_db.models import *

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
        print(counts_results)
        for result in counts_results:

            result_dict = result.get_result()

            if result_dict["counts_predicted"] is not None:
                try:
                    print(type(int(result_dict["counts_predicted"])))
                    average = (average + int(result_dict["counts_predicted"])) / 2
                    maximum = max(maximum, int(result_dict["counts_predicted"]))
                    minimum = min(minimum, int(result_dict["counts_predicted"]))
                except Exception:
                    print(result_dict)

        return {"day": results_by_day, "rooms_used": rooms_dict}