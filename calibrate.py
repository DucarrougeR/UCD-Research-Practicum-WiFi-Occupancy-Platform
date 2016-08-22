"""
Runs scripts to generate predictions for the entire database, calculate room and allocation scores and calibrate the sensor baselines in the database. 
"""
from app.mod_stat import *
from app.mod_sensors import *
from app.mod_db.models import *

predict.generate_scores()
predict.predict_all()
calibration.calibrate_baselines("app/mod_sensors/data/B002-21-08-2016-14-08-50.csv", "B002")
calibration.calibrate_baselines("app/mod_sensors/data/B003-21-08-2016-14-08-50.csv", "B003")
calibration.calibrate_baselines("app/mod_sensors/data/B004-21-08-2016-14-08-50.csv", "B004")

classes = Classes.select(Classes).where(Classes.classes_module_code != None)

rooms = Rooms.select(Rooms)
room_dict = {}

for room in rooms:
    room_dict[room.room_number] = room.room_capacity

for result in classes:
    if result.classes_size == None or result.classes_size == "":
        result.classes_size = 0
    try:
        result.classes_attendance_score = float(result.classes_size) / float(room_dict[result.classes_room_number])

    except Exception:
        print(result.classes_size)
    result.save()
