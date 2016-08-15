# Romain Ducarrouge

''' Generating Classes_Attendance_Score and Room_Occupancy_Score '''
import config
import sqlite3
import pandas as pd
import numpy as np

# Creates a direct SQL connection to database.
con1 = sqlite3.connect("analysis.db")    

# Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
df = pd.read_sql_query("SELECT * from Max_table", con1)

# Generate a new column, to use for generating score
df['room_allocation_score'] = np.nan
df['room_allocation_score'] = (df['counts_size']/df['counts_capacity'])*100

# Removing all rows without score
df = df.dropna(subset=['room_allocation_score'])


# Code to get the average allocation rating for rooms B002, B003, B004
df2 = df

df2 = df2.groupby([df2['counts_room']]).mean()

print(df2.room_allocation_score)



# Connect to Database.db to save the table
con = sqlite3.connect(config.DATABASE['name'])
cur = con.cursor()

df.to_sql('Allocation_Score', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

print("The room allocation scores were generated and saved in table 'Allocation_Score'")
