"""
Identifies rooms which are experiencing the "bleeding" effect, having clients associated to
the access point who are not not physically in the room. 
"""

import sqlite3
import pandas as pd

# Connects to the database. 
con = sqlite3.connect("../database.db")

# Finds rows in the database where ground truth is 0 but the model predicts 
# occupancy greater than 20. 
df = pd.read_sql_query("SELECT * from counts", con)
df = df[pd.notnull(df["counts_predicted"])]    
df = df[df["counts_truth"] == 0]
df = df[df["counts_predicted"] >= 20]

print("Problem rooms: ", df.counts_room_number.unique())
