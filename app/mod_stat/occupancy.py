import sqlite3
import pandas as pd
import statsmodels.formula.api as sm

# Creates a SQL connection to our SQLite database.
con = sqlite3.connect("../mod_db/database.db")

df = pd.read_sql_query("SELECT * from counts WHERE counts_time LIKE '%__:13:%' \
        OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
        OR counts_time LIKE '%__:17:%'", con)

# Changes the counts_truth column to float. 
df["counts_truth"] = df["counts_truth"].astype("float64")

# Looks only at columns with ground truth observations. 
df_obs = df[pd.notnull(df["counts_truth"])]

print(len(df.index))
"""
# Trains a linear regression model.
lm = sm.ols(formula="counts_truth ~  counts_associated", data=df).fit()

# Prints the coefficients and their significance levels. 
print(lm.summary())
"""

con.close()


