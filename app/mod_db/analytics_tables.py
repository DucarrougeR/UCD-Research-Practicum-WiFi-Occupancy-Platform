#Romain Ducarrouge

import sqlite3
import pandas as pd

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

# Merging two dataframes based on three keys 'Room', 'Date', 'Hour'.
Fixed_DF = pd.merge(occupancy_DF, Ass_Auth_DF, left_on=["room", "date", "hour"], right_on=["room", "date", "hour"],
                  how="outer", left_index=False, right_index=False)

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

# Drop redundant dataframe columns
Fixed_DF = Fixed_DF.drop("capacity_y",1).drop("time_0",1)

# Identify if columns only contain NaN value
for column in Fixed_DF.columns:
    if (Fixed_DF[column].isnull().all()):
        print("Column contains only NaN value")
    else:
        pass
print(Fixed_DF['occupancy'].isnull().all())
# Sorting the dataframe chronologically, by day, then by hour
Fixed_DF.sort(['date','hour'], axis=0, ascending=[True, True], inplace=False, kind='quicksort', na_position='last')

# print(Fixed_DF.shape)
Fixed_DF.head(250)

# Fixed_DF.loc[Fixed_DF['room'] != "B004"]

Fixed_DF.to_sql('cleaned_analysis_table', connect, flavor='sqlite', if_exists='replace',
          index=False, chunksize=None)

XP_Min = Fixed_DF.groupby([Fixed_DF['room'],Fixed_DF['date'], Fixed_DF['hour']]).min()
XP_Min.to_sql('Min_table', connect, flavor='sqlite', if_exists='replace',
              index=False, chunksize=None)
# XP_Min.head()

XP_Max = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour']]).max()
XP_Max.to_sql('Max_table', connect, flavor='sqlite', if_exists='replace',
              index=False, chunksize=None)

# XP_Max.head()

##########################################################################
'''MISSING DATA --- NEED TO ADD THE REMAINING INFO (day, hour...)'''
XP_Mean = Fixed_DF.groupby([Fixed_DF['room'],Fixed_DF['date'], Fixed_DF['hour']]).mean()
XP_Mean.to_sql('Mean_table', connect, flavor='sqlite', if_exists='replace',
               index=False, chunksize=None)
# XP_Mean.head()

XP_Med = Fixed_DF.groupby([Fixed_DF['room'],Fixed_DF['date'], Fixed_DF['hour']]).median()
XP_Med.to_sql('Med_table', connect, flavor='sqlite', if_exists='replace',
              index=False, chunksize=None)
# XP_Med.head()

# XP_Mode = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour']]).mode()
# XP_Mode = Fixed_DF.groupby([Fixed_DF['date'], Fixed_DF['hour']]).agg(pd.Series.mode)

# XP_Mode.to_sql('Mode_table', connect, flavor='sqlite', if_exists='replace',
#               index=False, chunksize=None)
# XP_Mode.head()


##########################################################################

# print("Tables saved")

print("Min table size is: " + str(XP_Min.shape))
print("Max table size is: " + str(XP_Max.shape))
print("Mean table size is: " + str(XP_Mean.shape))
print("Median table size is: " + str(XP_Med.shape))
# print("Need to Work on last 2 tables")
print('Min Table data is as follows \n --------------------------------------------------')
print(XP_Min.head())