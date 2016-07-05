import pandas as pd
import csv

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
result = pd.concat(dataframes, axis=1)

''' Stripping the whitespace in data for future Queries '''
result['campus'] = result['campus'].str.strip()
result['building'] = result['building'].str.strip()
result['room'] = result['room'].str.strip()

#Normalizing the room data field
result['room'] = result['room'].map(lambda x: x.replace('-', ''))

df_quarter = result.time.str.contains("... ... .. ...(13|14|15|16|17)... ......... ....", regex=True, na=False)
result = result[df_quarter]

''' Normalizing the Time data field for merging dataframe later on '''
#remove trailing string part
result['time'] = result['time'].map(lambda x: x.replace(' GMT+00:00 2015', ''))
#remove info about minutes and seconds
result['time'] = result['time'].map(lambda x: x[:-5])
#replace the minutes and seconds to identical format as other dataframes
result['time'] = result['time'].map(lambda x: x + '00:00')

#Renaming column to fix header
result.to_csv("data/clean/formattedLogs.csv")

# result.head()

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
  
    
    
##########################################################################

# FORMATTING TIME TABLE FILE
df3 = pd.read_csv("data/clean/timetable_clean.csv")

#Formatting 'None' value to NULL for future SQL queries
df3['module'].replace('None', "NULL", inplace=True)
df3['size'].replace('None', "NULL", inplace=True)
df3['size'].replace('N/A', 'NULL', inplace=True)

df3['room'] = df3['room'].map(lambda x: x.replace('.', ''))

df3.to_csv("data/clean/formattedTimeTable.csv", index=False)


##########################################################################

print('Data successfully cleaned')