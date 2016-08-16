#Romain Ducarrouge

import sqlite3
import pandas as pd
import config
import numpy as np

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

# df_quarter = df1.time.str.contains("... ... .. ...(13|14|15|16|17)"
#                                    "... ......... ....", regex=True, na=False)
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

# Converting last column to numeric to perform math operation
df2[['occupancyCount']] = df2[['occupancyCount']].apply(pd.to_numeric)

# Adding actual count value for room
df2['occupancyCount'] = df2['occupancyCount'] * df2['capacity'] / 100
df2['occupancy'] = df2['occupancy'].map(lambda x: x.replace('%', ''))

df2.to_csv("data/clean/formattedGroundTruthData.csv")

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
DF = pd.merge(d1, d2, left_on=["room", "time"], right_on=["room", "time"],
              how="outer", left_index=False, right_index=False)

DF.drop('Unnamed: 0_x', axis=1, inplace=True)
DF.drop('Unnamed: 0_y', axis=1, inplace=True)

d3 = pd.read_csv("data/clean/formattedTimeTable.csv")


DFinal = pd.merge(DF, d3, left_on=["room", "time"], right_on=["room", "time"],
                  how="outer", left_index=False, right_index=False)


DFinal['room'] = DFinal['room'].map(lambda x: x.replace('.', ''))
DFinal['room'] = DFinal['room'].map(lambda x: x.replace('-', ''))


# Adding a column for hour and one for date
C = (DFinal[['time']])
C['time'] = C['time'].map(lambda x: x[10:-6])
D = (DFinal[['time']])
D['time'] = D['time'].map(lambda x: x[8:-8])

DFinal['hour'] = C
DFinal['date'] = D
DFinal[['hour']] = DFinal[['hour']].apply(pd.to_numeric)
DFinal[['date']] = DFinal[['date']].apply(pd.to_numeric)

# Splitting XP dataframe into 2 separate df, one with no null data for occupancy,
# other with no null values for associated
DF_occupancy_Not_null = DFinal[DFinal['occupancy'].notnull()]
DF_data_Not_null = DFinal[DFinal['associated'].notnull()]

# Merging two dataframes based on three keys 'Room', 'Date', 'Hour'
dataframeFinal = pd.merge(DF_occupancy_Not_null, DF_data_Not_null, left_on=["room", "date", "hour"],
                    right_on=["room", "date", "hour"], how="outer",
                    left_index=False, right_index=False, copy=False)

for column in dataframeFinal.columns:
    if (dataframeFinal[column].isnull().all()):
        print("Contains only NaN values: " + column + "  ==> was dropped from dataframe")
        dataframeFinal = dataframeFinal.drop(column, axis=1)
    else:
        pass

dataframeFinal.loc[dataframeFinal['campus_y'] != "Belfield", 'campus_y'] = 'Belfield'
dataframeFinal.loc[dataframeFinal['building_y'] != "Computer Science", 'building_y'] = 'Computer Science'

dataframeFinal.time_y.fillna(dataframeFinal.time_x, inplace=True)

dataframeFinal = dataframeFinal.drop('time_x', axis=1)

dataframeFinal.columns = ['room', 'capacity', 'occupancy', 'occupancyCount',
       'module', 'size', 'hour', 'date', 'campus', 'building', 'time', 'associated',
       'authenticated']

dataframeFinal.sort(columns=["date","hour"], axis=0)

##########################################################################
''' Creating Dataframe to match DB schema's tables '''

Rooms_DB = DFinal[['room', 'building', 'campus', 'capacity']]

# Remove duplicates in dataframe
Rooms_DB = Rooms_DB.drop_duplicates(subset='room', keep='first')

Rooms_DB.loc[Rooms_DB.room == "B002", 'capacity'] = 90
Rooms_DB.loc[Rooms_DB.room == "B003", 'capacity'] = 90
Rooms_DB.loc[Rooms_DB.room == "B004", 'capacity'] = 160

Rooms_DB.loc[Rooms_DB.room == "B1.06", 'building'] = "Computer Science"
Rooms_DB.loc[Rooms_DB.room == "B1.06", 'campus'] = "Belfield"

Rooms_DB.loc[Rooms_DB.room == "B1.08", 'building'] = "Computer Science"
Rooms_DB.loc[Rooms_DB.room == "B1.08", 'campus'] = "Belfield"

Rooms_DB.loc[Rooms_DB.room == "B1.09", 'building'] = "Computer Science"
Rooms_DB.loc[Rooms_DB.room == "B1.09", 'campus'] = "Belfield"

Rooms_DB.columns = ["room_number", "room_building", "room_campus", "room_capacity"]
# using np.nan here since to_sql function will automatically write nan as NULL
Rooms_DB['room_occupancy_score'] = np.nan
Rooms_DB['room_rssi_baseline'] = np.nan
Rooms_DB['room_audio_baseline'] = np.nan

##########################################################################
Counts_DB = pd.read_csv('data/clean/DataForCountsTable.csv')

Counts_DB.time_0.fillna(Counts_DB.time, inplace=True)
# print(Counts_DB['counts_module_code'].isnull().all())
Counts_DB = Counts_DB.drop("Unnamed: 0", axis=1).drop("capacity", axis=1).drop("size", axis=1)
Counts_DB = Counts_DB.drop("hour", axis=1).drop("date", axis=1).drop("capacity_y", axis=1)
Counts_DB = Counts_DB.drop('time', axis=1)

# add column for 'counts_truth_is_occupied'
Counts_DB['counts_truth_is_occupied'] = np.nan

Counts_DB.loc[Counts_DB.occupancy == '25%', 'counts_truth_is_occupied'] = 1
Counts_DB.loc[Counts_DB.occupancy == '50%', 'counts_truth_is_occupied'] = 1
Counts_DB.loc[Counts_DB.occupancy == '75%', 'counts_truth_is_occupied'] = 1
Counts_DB.loc[Counts_DB.occupancy == '100%', 'counts_truth_is_occupied'] = 1
Counts_DB.loc[Counts_DB.occupancy == '0%', 'counts_truth_is_occupied'] = 0

Counts_DB.columns = ['counts_room_number', 'counts_truth_percent', 'counts_truth',
       'counts_module_code', 'counts_time', 'counts_associated', 'counts_authenticated','counts_truth_is_occupied']
# adding empty columns for model predictions on continuous and categorial features
Counts_DB['counts_predicted'] = np.nan
Counts_DB['counts_predicted_is_occupied'] = np.nan

##########################################################################
Classes_DB = DFinal[['room', 'time', 'module', 'size']]

Classes_DB['time'] = Classes_DB['time'].map(lambda x: x[:-5])
Classes_DB['time'] = Classes_DB['time']+"00:00"

Classes_DB.columns = ['classes_room_number', 'classes_time', 'classes_module_code', 'classes_size']
Classes_DB['classes_attendance_score'] = np.nan

Classes_DB.drop_duplicates(subset=['classes_room_number','classes_time'], keep='last')

#########################################################################
''' implementing tables for sensors '''

columns = ['sensors_room','sensors_time', 'sensors_rssi', 'sensors_audio', 'sensors_video']
Sensors_DB = pd.DataFrame(columns=columns)


'''
# Current table format is in 5-min interval as per initial discussion.
# Below is code to use to change the table to an hourly basis
Sensors_DB['checks_time'] = Sensors_DB['checks_time'].map(lambda x: x[:-6)		# removes seconds and minutes
Sensors_DB = Sensors_DB.drop_duplicates(subset='checks_time', keep='first')		# keeps 1 row per hour
'''

#########################################################################
''' Writting dataframe to sql files '''

con = sqlite3.connect(config.DATABASE['name'])
cur = con.cursor()
try:
	Rooms_DB.to_sql('rooms', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)
	Counts_DB.to_sql('counts', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)
	Classes_DB.to_sql('classes', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)
	Sensors_DB.to_sql('sensors', con, flavor='sqlite', if_exists='replace', index=False, chunksize=None)
except:
    print("Unexpected error writing table(s) to the Database")
    raise

	
print('Tables created')

