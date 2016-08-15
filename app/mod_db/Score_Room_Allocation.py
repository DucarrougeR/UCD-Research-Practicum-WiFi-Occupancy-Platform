# Romain Ducarrouge

''' Generating Classes_Attendance_Score and Room_Occupancy_Score '''
import sqlite3
import pandas as pd
import numpy as np

# Creates a direct SQL connection to database.
con = sqlite3.connect("analysis.db")    

# Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
df = pd.read_sql_query("SELECT * from Max_table", con)

df['room_allocation_score'] = np.nan
df['room_allocation_score'] = (df['counts_size']/df['counts_capacity'])*100


print(df.head(10))


#room_score = df[df["counts_predicted_is_occupied"] == 1.0]["counts_predicted_is_occupied"].count() / df["counts_predicted_is_occupied"].count()
# Records the score in the database. 
#query = Rooms.update(room_occupancy_score = room_score).where(Rooms.room_number == room)
#query.execute()