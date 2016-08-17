# from app.mod_stat import *
#
# predict.generate_scores()
# predict.predict_all()

from app.mod_db.models import *

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
