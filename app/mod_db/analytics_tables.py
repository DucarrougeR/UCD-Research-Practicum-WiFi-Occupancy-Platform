#Romain Ducarrouge

import sqlite3
import pandas as pd
import numpy as np
from scipy.stats.mstats import mode


DFinal = pd.read_csv("data/clean/FullyMergedDataframe.csv")

DFinal['room'].map(lambda x: x.replace('.', ''))
DFinal['room'].map(lambda x: x.replace('-', ''))

DFinal.loc[DFinal['campus'] != "Belfield", 'campus'] = 'Belfield'
DFinal.loc[DFinal['building'] != "Computer Science", 'building'] = 'Computer Science'

DFinal.loc[DFinal['room'] == "B002", 'capacity'] = 90
DFinal.loc[DFinal['room'] == "B003", 'capacity'] = 90
DFinal.loc[DFinal['room'] == "B004", 'capacity'] = 160

DFinal = DFinal.drop('Unnamed: 0', 1)

connect = sqlite3.connect("analysis.db")
cursor = connect.cursor()
DFinal.to_sql('analysis_table', connect, flavor='sqlite', if_exists='replace',
              index=False, chunksize=None)

try:
    XP = pd.read_sql_query("SELECT * \
                            FROM analysis_table \
                            WHERE associated IS NOT NULL \
                            OR occupancyCount IS NOT NULL", connect)
except:
    print("Unexpected Error Reading from Database")
    raise

# Adding a column for hour and one for date
C = (XP[['time']])
C['time'] = C['time'].map(lambda x: x[10:-6])
D = (XP[['time']])
D['time'] = D['time'].map(lambda x: x[8:-8])

XP['hour'] = C
XP['date'] = D
XP[['hour']] = XP[['hour']].apply(pd.to_numeric)
XP[['date']] = XP[['date']].apply(pd.to_numeric)

# Splitting XP dataframe into 2 separate df, one with no null data for occupancy,
# other with no null values for associated
occupancy_DF = XP[XP['occupancy'].notnull()]
Ass_Auth_DF = XP[XP['associated'].notnull()]

# Merging two dataframes based on three keys 'Room', 'Date', 'Hour'
Fixed_DF = pd.merge(occupancy_DF, Ass_Auth_DF, left_on=["room", "date", "hour"],
                    right_on=["room", "date", "hour"], how="outer",
                    left_index=False, right_index=False)

# Drop duplicate columns following dataframes' merged
Fixed_DF = Fixed_DF.drop("campus_x", 1).drop("building_x",1)
Fixed_DF = Fixed_DF.drop("campus_y", 1).drop("building_y",1)
Fixed_DF = Fixed_DF.drop("authenticated_x",1).drop("associated_x",1)
Fixed_DF = Fixed_DF.drop("occupancy_y",1).drop("occupancyCount_y",1).drop("module_y",1).drop("size_y",1)

# Renaming columns in the dataframe
Fixed_DF.columns = ['room', 'time', 'capacity', 'occupancy', 'occupancyCount',
       'module', 'size', 'hour', 'date', 'time_0', 'associated',
       'authenticated', 'capacity_y']

# Replacing NaN values in one Column by values of other column
Fixed_DF.capacity.fillna(Fixed_DF.capacity_y, inplace=True)
Fixed_DF.time.fillna(Fixed_DF.time_0, inplace=True)

Fixed_DF.to_csv('data/clean/DataForCountsTable.csv')

# Drop redundant dataframe columns
Fixed_DF = Fixed_DF.drop("capacity_y",1).drop("time_0",1)

# Identify if columns only contain NaN value
for column in Fixed_DF.columns:
    if (Fixed_DF[column].isnull().all()):
        print("Contains only NaN values: " + column)
    else:
        pass

# Sorting the dataframe chronologically, by day, then by hour
Fixed_DF.sort(['date','hour'], axis=0, ascending=[True, True], inplace=False,
              kind='quicksort', na_position='last')

Fixed_DF.to_sql('cleaned_analysis_table', connect, flavor='sqlite', if_exists='replace',
          index=False, chunksize=None)

'''  '''

XP_Min = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour'], Fixed_DF['room']]).min()
#XP_Min = XP_Min.drop('room_2', axis=1)
XP_Min['time'] = XP_Min['time'].map(lambda x: x[:-6])
XP_Min.to_sql('Min_table', connect, flavor='sqlite', if_exists='replace',
              index=True, chunksize=None)
# XP_Min.head()

XP_Max = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour'], Fixed_DF['room']])
XP_Max = XP_Max.max()
XP_Max['time'] = XP_Max['time'].map(lambda x: x[:-6])
XP_Max.to_sql('Max_table', connect, flavor='sqlite', if_exists='replace',
              index=True, chunksize=None)
# XP_Max.head()

XP_Mean = Fixed_DF
XP_Mean['time'] = XP_Mean['time'].map(lambda x: x[:-6])
XP_Mean = XP_Mean.groupby([Fixed_DF['time'], Fixed_DF['room']]).mean()
XP_Mean = XP_Mean.drop(['hour','date'], axis=1)
XP_Mean.to_sql('Mean_table', connect, flavor='sqlite', if_exists='replace',
               index=True, chunksize=None)
#XP_Mean.head()
			   
XP_Med = Fixed_DF
XP_Med = XP_Med.groupby([Fixed_DF['time'], Fixed_DF['room']]).median()
XP_Med = XP_Med.drop(['hour','date'], axis=1)
XP_Med.to_sql('Med_table', connect, flavor='sqlite', if_exists='replace',
              index=True, chunksize=None)
#XP_Med.head()


''' 
>>> Attempts to generate modal values table, 
>>> unsuccessful (multpile hourly observations)
>>> http://stackoverflow.com/questions/38594027/getting-the-maximum-mode-per-group-using-groupby/38594308?noredirect=1#comment64617825_38594308

# # XP_Mode = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour'], Fixed_DF['room']])
# XP_Mode = Fixed_DF
# # Using NumPy to consider only numeric number and not count NaN values
# XP_Mode = XP_Mode[np.isfinite(XP_Mode['associated'])]
# XP_Mode.groupby(lambda x: x.XP_Mode.date).agg(lambda x: stats.mode(x)[0][0])

# Using NumPy to consider only numeric number and not count NaNsvalues
# XP_Mode = XP_Mode[np.isfinite(XP_Mode['associated'])]
# Generate new Column with count of value occurrences (to use for mode)
# XP_Mode['count'] = XP_Mode['associated'].value_counts()
# Group by the 3 features, date, hour and room
# XP_Mode = XP_Mode.groupby([Fixed_DF['date'], Fixed_DF['hour'], XP_Mode['room']]).max()


# f = lambda x: mode(x, axis=1)[-1]
# XP_Mode = XP_Mode.groupby([XP_Mode['date'], XP_Mode['hour'], XP_Mode['room']]).apply(f)

# XP_Mode = XP_Mode.sort(columns='count', axis=1, ascending=False)

# XP_Mode.iloc[XP_Mode.groupby([XP_Mode['date'], XP_Mode['room']]).apply(lambda x: x['count'].idxmax())]

# XP_Mode.to_sql('Mode_table', connect, flavor='sqlite', if_exists='replace',
#               index=False, chunksize=None)
# XP_Mode.head()
'''
print("Finished")
