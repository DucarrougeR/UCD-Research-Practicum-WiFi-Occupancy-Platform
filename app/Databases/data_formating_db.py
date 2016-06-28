import pandas as pd
import csv

df = pd.read_csv("logs_clean.csv")

#Split first column into 3 columns of data (Campus, Building, Room)
New1 = Logs['room'].str.partition('>')
New1.columns = ['campus', 'building', 'room']

New2 = New1['room'].str.partition('>')
New2.columns = ['Building', '>>', 'Room']

New1['building'] = New2['Building']
New1['room'] = New2['Room']

df = df.drop(df.columns[[0]], axis=1)

#Concatenating the two new dataframes
dataframes = [New1, df]
result = pd.concat(dataframes, axis=1)

# Working on splitting the time fields for database
time = result['time']
t2 = result['time'].str.partition(' ')
t2.columns = ['day', 'space', 'rest']

t3 = t2['rest'].str.partition(' ')
t3.columns = ['month', 'space', 'rest']

t4 = t3['rest'].str.partition(' ')
t4.columns = ['date', 'space', 'rest']

t5 = t4['rest'].str.partition(' ')
t5.columns = ['time', 'space', 'rest']

t6 = t5['rest'].str.partition(' ')
t6.columns = ['gmt', 'space', 'year']

dfTime = [t2['day'], t3['month'], t4['date'], t5['time'], t6['year']]
newTime = pd.concat(dfTime, axis=1)

Data = [result['campus'],result['building'],result['room'], newTime, result['assocated'], result['authenticated']]
dataFinal = pd.concat(Data, axis=1)

#Renaming column to fix header
dataFinal = dataFinal.rename(columns = {'assocated':'associated'})

dataFinal.head()