from models import * 
import sqlite3

def fit_15():
    """
    Fits models using log files at xx:15 for every hour (corresponding 
    to the time the ground truth data was collected) and tests them on the data. 
    """
    
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../../mod_db/database.db")    

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

    #ols(df_obs, "plots/ols15.png", "plots/predictions_ols15.png")
    #ols_bin(df_obs, "plots/ols15_bin.png", "plots/predictions_ols15_bin.png")
    #logit(df_obs, "plots/predictions_logit.png")
    #ordlogit(df_obs)

def fit_15_outliers():
    """
    Drops rows with significant outliers and reruns the models. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../../mod_db/database.db")    

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
    
    # Fits the models. 
    ols(df_obs, "plots/ols15_outliers.png", "plots/predictions_ols15_outliers.png")
    ols_bin(df_obs, "plots/ols15_bin_outliers.png", "plots/predictions_ols15_bin_outliers.png")
    logit(df_obs, "plots/predictions_logit_outliers.png")
    ordlogit(df_obs)

    con.close()

def data_quality(df):
    """
    Data quality; descriptive statistics, 
    """
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../../mod_db/database.db")    

    print("""
    DATA QUALITY 
    ___________________________________
    """)

    df = pd.read_sql_query("SELECT * from counts", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with ground truth observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]

    # Lists descriptive statistics for the continuous features. 
    print("\nDescriptive statistics:")
    print(df_obs.describe().T)

    con.close()

def assoc_vs_authen():
    """
    Compares the "associated" and "authenticated" counts. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../../mod_db/database.db")    

    # Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
    df = pd.read_sql_query("SELECT * from counts WHERE counts_time LIKE '%__:13:%' \
            OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
            OR counts_time LIKE '%__:17:%'", con)
    
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../mod_db/database.db")    

    print("""
    COMPARING ASSOCIATED AND AUTHENTICATED COUNTS
    ___________________________________
    """)

    df = pd.read_sql_query("SELECT * from counts", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with ground truth observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]

    # Compares the associated and authenticated count correlation and prints outliers. 
    print("Correlation between \"associated\" and \"authenticated\" counts: ", df_obs["counts_associated"].corr(df_obs["counts_authenticated"]))
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_authenticated"])
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 3
    print("Associated count outiers (if any): \n", df_obs.loc[df_obs["counts_outliers"] == True], "\n")

    # Draws a scatterplot of associated count against ground truth count. 
    print("\nGenerating scatterplot...")
    plt.scatter(df_obs.counts_associated, df_obs.counts_truth,
            marker="o",
            edgecolor="b",
            facecolor="none",
            alpha=0.5 )
    plt.xlabel("Associated count")
    plt.ylabel("Truth count")
    plt.savefig("plots/associated-X-truth_scatter.png", fmt="png", dpi=100)

    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]    

    # Fits the linear model using associated count. 
    ols(df_obs, "plots/ols15_associated.png", "plots/predictions_ols15_outliers.png")
    
def time_window():
    """
    Determines the best time window to use for accurate predictions. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../../mod_db/database.db")    

    print("""
    CHOOSING A TIME WINDOW
    ___________________________________
    """)

    df = pd.read_sql_query("SELECT * from counts", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    con.close()


# Silences a pandas warning. 
pd.options.mode.chained_assignment = None

#data_quality()   
#assoc_vs_authen()
#time_window()
#fit_15()
#fit_15_outliers()


