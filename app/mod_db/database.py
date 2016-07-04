import pandas as pd
import re

# Opens the master log file CSV.  
df_logs = pd.read_csv("data/clean/logs_clean.csv")

# Drops any rows not near quarter past the hour (the time matching our ground truth data). 
df_quarter = df_logs.time.str.contains("... ... .. ...(13|14|15|16|17)... ......... ....", regex=True, na=False)
df_logs = df_logs[df_quarter]

# Opens the cleaned timetable CSV file.  
df_timetable = pd.read_csv("data/clean/timetable_clean.csv")

# Drop classes with no module code. 
bad = ["Career opportunities talks", "Booked by School of CS (no other data available"]
df_timetable = df_timetable[df_timetable.module != 0]
