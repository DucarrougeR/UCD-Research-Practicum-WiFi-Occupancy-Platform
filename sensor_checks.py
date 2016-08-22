import os, sqlite3, datetime
import pandas as pd
from app.mod_sensors import *
from app.mod_db.models import *

def checks():
    """
    Reads files containing sensor data recorded by the Raspberry Pi, checking the values therein
    against cutoff values to determine whether the sensors estimate that the room is occupied. 
    """

    # Cutoff levels for deviation from baselines. Need to be determined more rigorously in the future. 
    cutoff_rssi = 10
    cutoff_audio = 5

    # File path for data. 
    path = "app/mod_sensors/data"

    # Creates a SQL connection to database.
    con = sqlite3.connect("database.db")        

    # For every file in the data folder not starting with "read": 
    for i in os.listdir(path):
        if not i.startswith(".") and not i.startswith("read"):
            check_rssi, check_audio = 0, 0

            # Reads the file. 
            f = path + "/" + i
            df_read = pd.read_csv(f)
            
            # Extracts the room and time.
            room = df_read.iloc[0]["room"]
            month = df_read.iloc[-1]["month"]
            time = datetime.date(1900, month, 1).strftime('%b') + \
                    " " + str(df_read.iloc[-1]["date"]) + " " + df_read.iloc[-1]["time"]
            
            # Calculates average RSSI.
            rssi = df_read["rssi"].mean()

            # Calculates average amplitude. 
            amp = df_read["maxamp"].mean()

            # Reads the baselines from the database. 
            baseline_rssi = pd.read_sql_query("SELECT room_rssi_baseline FROM rooms WHERE room_number = '" + room + "'", con)
            baseline_audio = pd.read_sql_query("SELECT room_audio_baseline FROM rooms WHERE room_number = '" + room + "'", con)
            
            # Sensor check = 1 if difference between value and baseline is greater than the cutoff. 
            if rssi - baseline_rssi.iloc[0]["room_rssi_baseline"] > cutoff_rssi:
                check_rssi = 1
            if amp - baseline_audio.iloc[0]["room_audio_baseline"] > cutoff_audio: 
                check_audio = 1 

            # Declares the dataframe to write to the database. 
            df_write = pd.DataFrame(columns=("sensors_room", "sensors_time", "sensors_rssi", "sensors_audio", "sensors_video"))
            df_write.loc[0] = [room, time, check_rssi, check_audio, 0]

            # Writes values to the database. 
            df_write.to_sql("sensors", con, flavor="sqlite", if_exists="append", index=False, chunksize=None)

        # Writes "read" to the front of the name.
        readf = "read" + f
        os.rename(f, readf)
        
def check_integrity():
    """
    Finds observations in the database of "problem rooms" with 
    occupancy predicted but no sensor checks triggering and 
    changes them.
    """

    # Creates a SQL connection to database.
    con = sqlite3.connect("database.db")            
    
    # Rooms with a "leaking" effect, determined in /stats/problem_rooms.py.
    problem_rooms = ["B004", "B002", "B003"]

    # For each room:
    for room in problem_rooms:
        # Queries the database for that room where occupancy is predicted and time = xx:15.
        df_count = pd.read_sql_query(
        "SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_time LIKE '%09:__:%' \
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%10:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%11:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%12:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%13:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%14:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%15:__:%'\
        UNION SELECT * FROM counts WHERE counts_room_number = '" + room + "' AND counts_predicted_is_occupied = 1 AND counts_time LIKE '%16:__:%'", con)

        # Reads the sensors table for corresponding observations. 
        df_sensors 

        # Changes counts_predicted_is_occupied to 0 where sensor checks are 0. 
