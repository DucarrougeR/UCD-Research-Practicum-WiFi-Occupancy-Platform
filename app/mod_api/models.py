# Luke Kearney
import re
import config

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
