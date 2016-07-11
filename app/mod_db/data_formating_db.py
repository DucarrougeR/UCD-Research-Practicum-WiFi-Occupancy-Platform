#Romain Ducarrouge

import pandas as pd
import csv
import sqlite3

# FORMATTING LOGS FILE
df = pd.read_csv("data/clean/logs_clean.csv")
#Split first column into 3 columns of data (Campus, Building, Room)
New1 = df['room'].str.partition('>')
New1.columns = ['campus', 'building', 'room']

New2 = New1['room'].str.partition('>')
New2.columns = ['Building', '>>', 'Room']
New1['building'] = New2['Building']
New1['room'] = New2['Room']

df = df.drop(df.columns[[0]], axis=1)

#Concatenating the two new dataframes
dataframes = [New1, df]
df1 = pd.concat(dataframes, axis=1)

''' Stripping the whitespace in data for future Queries '''
df1['campus'] = df1['campus'].str.strip()
df1['building'] = df1['building'].str.strip()
df1['room'] = df1['room'].str.strip()

#Normalizing the room data field
df1['room'] = df1['room'].map(lambda x: x.replace('-', ''))

# df_quarter = df1.time.str.contains("... ... .. ...(13|14|15|16|17)... ......... ....", regex=True, na=False)
# df1 = df1[df_quarter]

''' Normalizing the Time data field for merging dataframe later on '''
#remove trailing string part
df1['time'] = df1['time'].map(lambda x: x.replace(' GMT+00:00 2015', ''))


df1.to_csv("data/clean/formattedLogs.csv")
print('Logs data has been cleaned')

##########################################################################

# FORMATTING GROUND TRUTH FILE
df2 = pd.read_csv("data/clean/gt_clean.csv")
df2['occupancyCount'] = df2['occupancy'].map(lambda x: x.replace('%', ''))

# Converting last column to numeric to perfomr math operation
df2[['occupancyCount']] = df2[['occupancyCount']].apply(pd.to_numeric)

# Adding actual count value for room
df2['occupancyCount'] = df2['occupancyCount'] * df2['capacity'] /100

df2.to_csv("data/clean/formattedGroundTruthData.csv")
#df2.head()
print('Ground Truth Data has been cleaned')

##########################################################################

# FORMATTING TIME TABLE FILE
df3 = pd.read_csv("data/clean/timetable_clean.csv")

#Formatting 'None' value to NULL for future SQL queries
df3['module'].replace('None', "NULL", inplace=True)
df3['size'].replace('None', "NULL", inplace=True)
df3['size'].replace('N/A', 'NULL', inplace=True)

df3['room'] = df3['room'].map(lambda x: x.replace('.', ''))

df3.to_csv("data/clean/formattedTimeTable.csv", index=False)
print('Time Table data successfully cleaned')

##########################################################################
''' Merging all dataframes '''

d1 = pd.read_csv("data/clean/formattedLogs.csv")
d2 = pd.read_csv("data/clean/formattedGroundTruthData.csv")
DF = pd.merge(d1, d2, left_on=["room",'time'], right_on=["room", "time"], how='outer', left_index=False, right_index=False)

DF.drop('Unnamed: 0_x', axis=1, inplace=True)
DF.drop('Unnamed: 0_y', axis=1, inplace=True)
# DF.head(50)

d3 = pd.read_csv("data/clean/formattedTimeTable.csv")
# d3.head()
DFinal =  pd.merge(DF, d3, left_on=["room",'time'], right_on=["room", "time"], how='outer', left_index=False, right_index=False)

# DFinal.head(50)


##########################################################################
''' Creating Dataframe to match DB schema's tables '''

Rooms_DB = DFinal[['room','building','campus','capacity']]

# Remove duplicates in dataframe
Rooms_DB = Rooms_DB.drop_duplicates(subset='room', keep='first')

Rooms_DB.loc[Rooms_DB.room == "B002", 'capacity'] = 90
Rooms_DB.loc[Rooms_DB.room == "B003", 'capacity'] = 90
Rooms_DB.loc[Rooms_DB.room == "B004", 'capacity'] = 160

Rooms_DB.loc[Rooms_DB.room == "B1.06", 'building'] = "Computer Science"
Rooms_DB.loc[Rooms_DB.room == "B1.06", 'campus'] = "Belfield"

Rooms_DB.loc[Rooms_DB.room == "B1.08", 'building'] = "Computer Science"
Rooms_DB.loc[Rooms_DB.room == "B1.08", 'campus'] = "Belfield"

Rooms_DB.columns = ["room_number", "room_building", "room_campus", "room_capacity"]
# Rooms_DB.head()

Counts_DB = DFinal[['room', 'time', 'module', 'associated', 'authenticated', 'occupancy', 'occupancyCount']]
Counts_DB.columns = ['counts_room_number', 'counts_time', 'counts_module_code', 'counts_associated', 'counts_authenticated', 'counts_truth_percent', 'counts_truth']
# Counts_DB.head()

Classes_DB = DFinal[['room', 'time', 'module', 'size']]
Classes_DB.columns = ['classes_module_code', 'classes_time', 'classes_room_number', 'classes_size']
# ''' No need to change the 'NaN' values
# to_sql supports writing NaN values (will be written as NULL) '''
# Classes_DB.head()

##########################################################################
''' Writting dataframe to sql files '''

con = sqlite3.connect('database.db')
cur= con.cursor()

Rooms_DB.to_sql('rooms', con,  flavor='sqlite', if_exists='replace', index=False, chunksize=None)
Counts_DB.to_sql('counts', con,  flavor='sqlite', if_exists='replace', index=False, chunksize=None)
Classes_DB.to_sql('classes', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

print('Tables created')
