#Romain Ducarrouge

import sqlite3
import pandas as pd
import config
import numpy as np

DFinal = pd.read_csv("data/clean/FullyMergedDataframe.csv")

DFinal['room'].map(lambda x: x.replace('.', ''))
DFinal['room'].map(lambda x: x.replace('-', ''))

DFinal.loc[DFinal['campus'] != "Belfield", 'campus'] = 'Belfield'
DFinal.loc[DFinal['building'] != "Computer Science", 'building'] = 'Computer Science'

DFinal.loc[DFinal['room'] == "B002", 'capacity'] = 90
DFinal.loc[DFinal['room'] == "B003", 'capacity'] = 90
DFinal.loc[DFinal['room'] == "B004", 'capacity'] = 160

connect = sqlite3.connect("analysis.db")
cursor = connect.cursor()
DFinal.to_sql('analysis_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

try:
    XP = pd.read_sql_query("SELECT * FROM analysis_table WHERE associated IS NOT NULL \
                                                        AND authenticated IS NOT NULL", connect)
except:
    print("Unexpected error connecting to database")
    raise

XP['day'], XP['month'], XP['date'], XP['hour'] = zip(*XP['time'].map(lambda x: x.split(' ')))
XP['hour'].map(lambda x: x[:-6])

XP.to_sql('cleaned_analysis_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

XP_Min = XP.groupby([XP['date'], XP['hour']]).min()
XP_Min.to_sql('Min_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

XP_Max = XP.groupby([XP['date'], XP['hour']]).max()
XP_Max.to_sql('Max_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

####################################################################################################
'''MISSING DATA --- NEED TO ADD THE REMAINING INFO (day, hour...)'''
XP_Mean = XP.groupby([XP['date'], XP['hour']]).mean()
XP_Mean.to_sql('Mean_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)

XP_Med = XP.groupby([XP['date'], XP['hour']]).median()
XP_Med.to_sql('Med_table', connect, flavor='sqlite', if_exists='replace', index=False, chunksize=None)
####################################################################################################

print('Tables saved')

print("Min table size is: " + str(XP_Min.shape))
print("Max table size is: " + str(XP_Max.shape))
print("Mean table size is: " + str(XP_Mean.shape))
print("Median table size is: " + str(XP_Med.shape))
print('Need to Work on last 2 tables')
