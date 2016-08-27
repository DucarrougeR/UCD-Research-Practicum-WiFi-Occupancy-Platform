#Romain Ducarrouge

import sqlite3
import pandas as pd

dfCount = pd.read_csv("data/rssi/HeadCount_7_27_16.csv")
dfRSSI = pd.read_csv("data/rssi/RSSI_data1.csv")

# Splitting the time feature into separate fields
dfRSSI['time'] = dfRSSI['time'].apply(lambda x: x[:-3])
dfRSSI['hour'] = dfRSSI['time'].apply(lambda x: x[:2])
dfRSSI['min'] = dfRSSI['time'].apply(lambda x: x[-2:])
dfRSSI = dfRSSI.drop('time', axis=1)

# Removing first observation per minute, get both dataframes with 1 observation/minute 
dfRSSI = dfRSSI.drop_duplicates(subset=['date','hour','min'], keep='last')

# Modifying the Date field into the same format
dfCount['month'] = dfCount['Date'].apply(lambda x: x[:1])
dfCount['date'] = dfCount['Date'].apply(lambda x: x[2:4])
dfCount['year'] = 2016
dfCount = dfCount.drop('Date', axis=1)
dfCount = dfCount.drop(['month','year'], axis=1)
dfRSSI = dfRSSI.drop(['month','year'], axis=1)

dfCount['hour'].astype(int)
dfCount['min'].astype(int)
dfCount['date'].astype(int)
dfRSSI['hour'].astype(int)
dfRSSI['min'].astype(int)
dfRSSI['date'].astype(int)

# resetting index on RSSI dataframe (after dropping half observations) for merging purposes
dfRSSI = dfRSSI.reset_index()

# merging dataframes
dataframe = pd.merge(dfCount, dfRSSI , on=['hour','min','date'],
                     left_index=True, right_index=True, how='outer')
dataframe = dataframe.drop('index', axis=1)

dataframe.to_csv("data/rssi/finalData1_HeadCount.csv")

# dataframe.head()



