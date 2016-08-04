"""
Determining the most predictive model specification. 
"""
from model_fitting import *
import sqlite3

def fit_15():
    """
    Fits models using log files at xx:15 for every hour (corresponding 
    to the time the ground truth data was collected) and tests them on the data. 
    """

    print("""
    RUNNING MODELS AT XX:15 TIME 
    ___________________________________
    """)
    
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")    

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

    # List to store outputs.
    outputs = []
    
    # Fits the models. 
    outputs.append(ols(df_obs, "plots/ols15.png", "plots/predictions_ols15.png"))
    outputs.append(ols_bin(df_obs, "plots/ols15_bin.png", "plots/predictions_ols15_bin.png"))
    outputs.append(logit(df_obs, "plots/predictions_logit.png"))
    outputs.append(ordlogit(df_obs))
    
    best_model = outputs[0]
    for i in range(0, len(outputs)):
        if outputs[i][2] > best_model[2]:
            best_model = outputs[i]

    print("Most predictive model: ", best_model)

def fit_15_outliers():
    """
    Drops rows with significant outliers and reruns the models. 
    """

    print("""
    RUNNING MODELS AT XX:15 TIME WITHOUT OUTLIERS
    ___________________________________
    """)

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")    

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
    
    # List to store outputs.
    outputs = []

    # Fits the models and stores the results in the list. 
    #outputs.append(ols(df_obs, "plots/ols15_outliers.png", "plots/predictions_ols15_outliers.png"))
    #outputs.append(ols_bin(df_obs, "plots/ols15_bin_outliers.png", "plots/predictions_ols15_bin_outliers.png"))
    #outputs.append(logit(df_obs, "plots/predictions_logit_outliers.png"))
    outputs.append(ordlogit(df_obs))

    best_model = outputs[0]
    for i in range(0, len(outputs)):
        if outputs[i][2] > best_model[2]:
            best_model = outputs[i]

    print("Most predictive model: ", best_model)

    con.close()

def assoc_vs_authen():
    """
    Compares the "associated" and "authenticated" counts. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")    

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

    # Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
    df = pd.read_sql_query("SELECT * from counts WHERE counts_time LIKE '%__:13:%' \
            OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
            OR counts_time LIKE '%__:17:%'", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with ground truth observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    

    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]    

    # Fits the linear model using associated count. 
    assoc_ols = ols(df_obs, "plots/ols15_assoc.png", "plots/predictions_ols15_assoc.png")

    # Refits the linear model using authenticated count. 
    authen_ols = ols_authen(df_obs, "plots/ols15_authen.png", "plots/predictions_ols15_authen.png")

    print("Associated count R-squared: ", assoc_ols[0])    
    print("Authenticated count R-squared: ", authen_ols[0])

    
def time_window():
    """
    Determines the best 5-minute time window to use for accurate predictions. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")    

    print("""
    DETERMINING THE OPTIMAL TIME WINDOW
    ___________________________________
    """)

    print("Running models in 5-minute windows")
    
    # Lists to store regression outputs.
    outputs_ols, outputs_ols_bin, outputs_logit, outputs_ordlogit = [], [], [], []
    
    # List of times in an hour in five-minute intervals. 
    times = []
    for i in range(3, 58):
        if i < 10:
            times.append("0" + str(i))
        else:
            times.append(str(i))
    
    # For each five-minute window in the database. 
    for i in range(0, len(times), 5):
        print(times[i], times[i+1], times[i+2], times[i+3], times[i+4])
        # Reads the database. 
        query = "SELECT * from counts WHERE counts_time LIKE '%__:(" + str(times[i]) + ":%' \
                OR counts_time LIKE '%__:" + str(times[i+1]) + ":%' OR counts_time LIKE '%__:" + str(times[i+2]) + ":%' \
                OR counts_time LIKE '%__:" + str(times[i+3]) +":%'\
                OR counts_time LIKE '%__:" + str(times[i+4]) + ":%'"
        df = pd.read_sql_query(query, con)    

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

        # Fits the models and stores the results in the relevant list. 
        outputs_ols.append(ols(df_obs, "plots/ols_window_outliers.png", "plots/predictions_ols_window_utliers.png"))
        outputs_ols_bin.append(ols_bin(df_obs, "plots/ols_window_bin_outliers.png", "plots/predictions_ols_window_bin_outliers.png"))
        outputs_logit.append(logit(df_obs, "plots/predictions_logit_window_outliers.png"))
        outputs_ordlogit.append(ordlogit(df_obs))
        
    # Loops over all the lists of outputs and finds the most predictive model. 
    best_ols = outputs_ols[0]
    best_ols_time = ""
    for i in range(0, len(outputs_ols)):
        if outputs_ols[i][2] > best_ols[2]:
            best_ols = outputs_ols[i]
    best_ols_bin = outputs_ols_bin[0]
    for i in range(0, len(outputs_ols_bin)):
        if outputs_ols_bin[i][2] > best_ols_bin[2]:
            best_ols_bin = outputs_ols_bin[i]
    best_logit = outputs_logit[0]
    for i in range(0, len(outputs_logit)):
        if outputs_logit[i][2] > best_logit[2]:
            best_logit = outputs_logit[i]
    """
    best_ordlogit = outputs_ols[0]
    for i in range(0, len(outputs_ordlogit)):
        if outputs_ordlogit[i][2] > best_ordlogit[2]:
            best_ordlogit = outputs_ordlogit[i]
    """
    
    print("\nOUTPUT\n")
    print("Most predictive OLS model: ", best_ols)
    print("Most predictive OLS model (with bins): ", best_ols_bin)
    print("Most predictive Logit model: ", best_logit)
    print("Most predictive Ordinal Logit model: ", best_ordlogit)    

    con.close()

def agg_count():
    """
    Specifies models based on aggregated counts (max, mean, median, mode) and 
    tests them on the data. 
    """

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../analysis.db")    

    print("""
    SPECIFYING MODELS BASED ON AGGREGATED COUNTS (MAX, MEAN, MEDIAN, MODE)
    ___________________________________
    """)

    # Lists to store regression outputs.
    outputs_ols, outputs_ols_bin, outputs_logit, outputs_ordlogit = [], [], [], []
    
    print("MAXIMUM COUNT")

    # Reads the database. 
    query = "SELECT * from Max_table"
    df = pd.read_sql_query(query, con)    

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    
    df_obs = df_obs[pd.notnull(df["counts_associated"])]    

    # Formats the counts_truth_percent column.
    df_obs["counts_truth_percent"] = df_obs["counts_truth_percent"].map(lambda x: x.replace("%", ""))
    df_obs.replace(to_replace={"counts_truth_percent" : {'0': 0, '25': 25, '50': 50, '75': 75, '100':100}}, inplace = True)    
    
    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]

    # Fits the models and stores the results in the relevant list. 
    outputs_ols.append("MAX")
    outputs_ols.append(ols(df_obs, "plots/ols_max_outliers.png", "plots/predictions_ols_max_utliers.png"))
    outputs_ols_bin.append("MAX")    
    outputs_ols_bin.append(ols_bin(df_obs, "plots/ols_max_bin_outliers.png", "plots/predictions_ols_max_bin_outliers.png"))
    outputs_logit.append("MAX")    
    outputs_logit.append(logit(df_obs, "plots/predictions_logit_max_outliers.png"))
    outputs_ordlogit.append("MAX")    
    outputs_ordlogit.append(ordlogit(df_obs))

    print("MEAN COUNT")

    # Reads the database. 
    query = "SELECT * from Mean_table"
    df = pd.read_sql_query(query, con)    

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    
    df_obs = df_obs[pd.notnull(df["counts_associated"])]    

    # Formats the counts_truth_percent column.
    df_obs["counts_truth_percent"] = df_obs["counts_truth_percent"].map(lambda x: x.replace("%", ""))
    df_obs.replace(to_replace={"counts_truth_percent" : {'0': 0, '25': 25, '50': 50, '75': 75, '100':100}}, inplace = True)    
    
    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]

    # Fits the models and stores the results in the relevant list. 
    outputs_ols.append("MEAN")
    outputs_ols.append(ols(df_obs, "plots/ols_mean_outliers.png", "plots/predictions_ols_mean_utliers.png"))
    outputs_ols_bin.append("MEAN")    
    outputs_ols_bin.append(ols_bin(df_obs, "plots/ols_mean_bin_outliers.png", "plots/predictions_ols_mean_bin_outliers.png"))
    outputs_logit.append("MEAN")    
    outputs_logit.append(logit(df_obs, "plots/predictions_logit_mean_outliers.png"))
    outputs_ordlogit.append("MEAN")    
    outputs_ordlogit.append(ordlogit(df_obs))

    print("MEDIAN COUNT")

    # Reads the database. 
    query = "SELECT * from Med_table"
    df = pd.read_sql_query(query, con)    

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    
    df_obs = df_obs[pd.notnull(df["counts_associated"])]    

    # Formats the counts_truth_percent column.
    df_obs["counts_truth_percent"] = df_obs["counts_truth_percent"].map(lambda x: x.replace("%", ""))
    df_obs.replace(to_replace={"counts_truth_percent" : {'0': 0, '25': 25, '50': 50, '75': 75, '100':100}}, inplace = True)    
    
    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]

    # Fits the models and stores the results in the relevant list. 
    outputs_ols.append("MEDIAN")
    outputs_ols.append(ols(df_obs, "plots/ols_median_outliers.png", "plots/predictions_ols_median_utliers.png"))
    outputs_ols_bin.append("MEDIAN")
    outputs_ols_bin.append(ols_bin(df_obs, "plots/ols_median_bin_outliers.png", "plots/predictions_ols_median_bin_outliers.png"))
    outputs_logit.append("MEDIAN")
    outputs_logit.append(logit(df_obs, "plots/predictions_logit_median_outliers.png"))
    outputs_ordlogit.append("MEDIAN")    
    outputs_ordlogit.append(ordlogit(df_obs))
    
    # Loops over all the lists of outputs and finds the most predictive model. 
    best_ols = outputs_ols[1]
    best_ols_bin = outputs_ols_bin[1]
    best_logit = outputs_logit[1]
    best_ordlogit = outputs_ordlogit[1]
    best_ols_type, best_ols_bin_type, best_logit_type, best_ordlogit_type = "", "", "", ""

    for i in range(1, len(outputs_ols), 2):
        if outputs_ols[i][2] > best_ols[2]:
            best_ols = outputs_ols[i]
            best_ols_type = outputs_ols[i-1]
    for i in range(1, len(outputs_ols_bin), 2):
        if outputs_ols_bin[i][2] > best_ols_bin[2]:
            best_ols_bin = outputs_ols_bin[i]
            best_ols_bin_type = outputs_ols_bin[i-1]
    for i in range(1, len(outputs_logit), 2):
        if outputs_logit[i][2] > best_logit[2]:
            best_logit = outputs_logit[i]
            best_logit_type = outputs_logit[i-1]
    """
    for i in range(0, len(outputs_ordlogit)):
        if outputs_ordlogit[i][2] > best_ordlogit[2]:
            best_ordlogit = outputs_ordlogit[i]
            best_ordlogit_type = outputs_ordlogit[i-1]
    """
    
    print("\nOUTPUT\n")
    print("Most predictive OLS model: ", best_ols, best_ols_type)
    print("Most predictive OLS model (with bins): ", best_ols_bin, best_ols_bin_type)
    print("Most predictive Logit model: ", best_logit, best_logit_type)
    #print("Most predictive Ordinal Logit model: ", best_ordlogit, best_ordlogit_type)    

    con.close()
    
def room_model():
    """
    Fits a different model for each room at xx:15 for every hour (corresponding to the time the ground
    truth data was collected) and tests it on the data. 
    """

    print("""
    RUNNING MODELS FOR EACH ROOM AT XX:15 TIME (OUTLIERS REMOVED)
    ___________________________________
    """)

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")        
    
    # Reads list of rooms from the database. 
    rooms = pd.read_sql_query("SELECT DISTINCT counts_room_number FROM counts", con)
    print("Rooms:\n\n", rooms["counts_room_number"])

    # Lists for outputs.
    outputs_ols, outputs_ols_bin, outputs_logit, outputs_ordlogit = [], [], [], []

    # For each room in the list:
    for room in rooms["counts_room_number"]:
        # Reads the database at xx:15 for every hour for that room. 
        query = "SELECT * from counts WHERE counts_room_number = '" + room + "' AND counts_time LIKE '%__:13:%'\
                OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
                OR counts_time LIKE '%__:17:%'"
        df = pd.read_sql_query(query, con)                    

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

        # Fits the models and prints the results. 
        print("MODELS FOR " + room + ":")        
        outputs_ols.append((ols(df_obs, "plots/ols_" + room + "_outliers.png", "plots/predictions_ols_" + room + "_outliers.png")))
        outputs_ols_bin.append((ols_bin(df_obs, "plots/ols_" + room + "_bin_outliers.png", "plots/predictions_ols_" + room + "_bin_outliers.png")))
        outputs_logit.append((logit(df_obs, "plots/predictions_logit_" + room + "_outliers.png")))
        #outputs_ordlogit.append((ordlogit(df_obs))

        print("OUTPUTS:\n", outputs_ols_bin)

    con.close()

def module_model():
    """
    Fits a different model for each module at xx:15 for every hour (corresponding to the time the ground
    truth data was collected) and tests it on the data. 

    """

    print("""
    RUNNING MODELS FOR EACH MODULE AT XX:15 TIME (OUTLIERS REMOVED)
    ___________________________________
    """)

    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")        

    # Reads list of modules from the database. 
    modules = pd.read_sql_query("SELECT DISTINCT counts_module_code FROM counts", con)
    print("Modules:\n\n", modules["counts_module_code"])

    # Lists for outputs.
    outputs_ols, outputs_ols_bin, outputs_logit, outputs_ordlogit = [], [], [], []    

    # For each module in the list:
    for module in modules["counts_module_code"]:
        # Ignores "None". 
        if module == None:
            continue 

        # Reads the database at xx:15 for every hour for that room. 
        query = "SELECT * from counts WHERE counts_module_code = '" + module + "' AND counts_time LIKE '%__:13:%'\
                OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
                OR counts_time LIKE '%__:17:%'"
        df = pd.read_sql_query(query, con)                    

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

        # Fits the models and prints the results. 
        print("MODELS FOR " + module + ":")        
        outputs_ols.append((ols(df_obs, "plots/ols_" + module + "_outliers.png", "plots/predictions_ols_" + module + "_outliers.png")))
        outputs_ols_bin.append((ols_bin(df_obs, "plots/ols_" + module + "_bin_outliers.png", "plots/predictions_ols_" + module + "_bin_outliers.png")))
        outputs_logit.append((logit(df_obs, "plots/predictions_logit_" + module + "_outliers.png")))
        #outputs_ordlogit.append((ordlogit(df_obs))
    
    print("OUTPUTS:\n", outputs_ols)

    con.close()

def binary_model():
    """
    Fits a binary model using log files at xx:15 for every hour (corresponding to the time the ground 
    truth data was collected) and tests it on the data. 
    """

    print("""
    RUNNING BINARY MODEL AT XX:15 TIME (OUTLIERS REMOVED)
    ___________________________________
    """)
    
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../database.db")    

    # Reads the database at xx:15 for every hour (corresponding to the time the ground truth data was collected). 
    df = pd.read_sql_query("SELECT * from counts WHERE counts_time LIKE '%__:13:%' \
            OR counts_time LIKE '%__:14:%' OR counts_time LIKE '%__:15:%' OR counts_time LIKE '%__:16:%'\
            OR counts_time LIKE '%__:17:%'", con)

    # Changes the counts_truth column to float. 
    df["counts_truth"] = df["counts_truth"].astype("float64")

    # Looks only at columns with ground truth observations. 
    df_obs = df[pd.notnull(df["counts_truth"])]    

    # Compares ground_truth to counts_associated to find large outliers. 
    df_obs["counts_difference"] = abs(df_obs["counts_associated"] - df_obs["counts_truth"])    
    df_obs["counts_outliers"] = abs(df_obs["counts_difference"]) > 20 # Cutoff determined through trial and error
    
    # Drops outlier rows.
    df_obs = df_obs[df_obs["counts_outliers"] == False]

    # Constructs a binary version of the truth count. 
    df_obs["counts_truth_is_occupied"] = df_obs["counts_truth"] > 0

    # Fits the model. 
    print(binarylogit(df_obs))

    con.close()

# Silences a pandas warning. 
pd.options.mode.chained_assignment = None

#fit_15()
#fit_15_outliers()
#assoc_vs_authen()
#time_window()
agg_count()
#room_model()
#module_model()
#binary_model()
