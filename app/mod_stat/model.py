import sqlite3
import pandas as pd
import statsmodels.formula.api as sm
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib

def train_ols():
    """
    Trains a simple OLS model on ground-truth count. 
    Serialises the output to a pickle file. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("database.db")    

    # Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
    df = pd.read_sql_query("SELECT * from counts WHERE counts_time LIKE '%__:13:%' \
            OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
            OR counts_time LIKE '%__:17:%'", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with ground truth observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    

    # Formats the counts_truth_percent column.
    df_obs["counts_truth_percent"] = df_obs["counts_truth_percent"].map(lambda x: x.replace("%", ""))
    df_obs.replace(to_replace={"counts_truth_percent" : {'0': 0, '25': 25, '50': 50, '75': 75, '100':100}}, inplace = True)    
    
    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]
    
    # Fits the linear model. 
    y = df_obs["counts_truth"]
    X = np.array(df_obs["counts_associated"].reshape(-1, 1))
    lrm = LinearRegression()    
    lrm.fit(X, y)

    # Serialises the fitted regression to disk. 
    joblib.dump(lrm, "app/mod_stat/model.pkl") 

# Silences a pandas warning. 
pd.options.mode.chained_assignment = None
