"""
Regression model specifications. 
"""
import sqlite3
import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import train_test_split    
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import sklearn.metrics as metrics

def ols(df, lsplot_path, predplot_path):
    """
    Fits a simple OLS model on ground-truth count and tests it on the data. 
    Arguments: dataframe, file path to save the least-squares plot, file path to
    save predictions plot. 
    Returns a list containing the model R-squared, the overall model significance,
    the explained variance score and the time of query. 
    """

    print("""
    LINEAR MODEL 
    ___________________________________
    """)

    # Stores the time for output.
    query_time = df.counts_time.max()

    # Trains the model and prints the output. 
    lrm = sm.ols(formula="counts_truth ~  counts_associated", data=df).fit()
    print(lrm.summary())

    # Separately prints the model R-squared, P-values, confidence intervals and overall model significance. . 
    print("Model R-squared: ", lrm.rsquared)
    print("P-values:\n", lrm.pvalues)
    print("Confidence interval for model coefficients:\n", lrm.conf_int())    
    model_p = lrm.f_pvalue
    print("Overall model significance: ", model_p)

    # Creates a dataframe with the minimum and maximum values of counts_associated.
    df_minmax = pd.DataFrame({"counts_associated": [df.counts_associated.min(), df.counts_associated.max()]})

    # Makes predictions for those values.
    preds = lrm.predict(df_minmax)

    # Plots the observed data.  
    df.plot(kind="scatter", x="counts_associated", y="counts_truth")

    # Plots the least-squares line. 
    plt.plot(df_minmax, preds, c="red", linewidth=2)
    plt.savefig(lsplot_path, fmt="png", dpi=100)

    # Re-runs the regression using scikit-learn. 
    print("\nSCIKIT")    
    y = df["counts_truth"]
    X = np.array(df["counts_associated"].reshape(-1, 1))
    lrm = LinearRegression()    

    lrm.fit(X, y)

    # Prints the model R-squared. 
    rsquared = lrm.score(X, y)
    print("Model R-squared: ", rsquared)
    
    # Splits the dataset into 60% training and 40% testing. 
    df_train, df_test = train_test_split(df, test_size = 0.4, random_state = 5)

    # Trains model on the training set.
    y_train = df_train["counts_truth"]
    X_train = np.array(df_train["counts_associated"].reshape(-1, 1))    
    lrm_train = LinearRegression()
    lrm_train.fit(X_train, y_train)
    
    # Tests model on the test set. 
    y_test = df_test["counts_truth"]
    X_test = np.array(df_test["counts_associated"].reshape(-1, 1))    
    # Prints mean-squared error (MSE).  
    print("Residual sum of squares: %.2f" % np.mean((lrm_train.predict(X_test) - y_test) ** 2))
    # Prints explained variance score (1 is perfect prediction). 
    vscore = lrm_train.score(X_test, y_test)
    print('Variance score (1 = perfect prediction): %.2f' % vscore)

    # Plots outputs.
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, lrm_train.predict(X_test), color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.savefig(predplot_path, fmt="png", dpi=100)

    return [rsquared, model_p, vscore, query_time]

def ols_authen(df, lsplot_path, predplot_path):
    """
    Fits a simple OLS model on ground-truth count 
    using authenticated count and tests it on the data. 
    Arguments: dataframe, file path to save the least-squares plot, file path to
    save predictions plot. 
    Returns a list containing the model R-squared, the overall model significance,
    the explained variance score and the time of query. 
    """

    print("""
    LINEAR MODEL 
    ___________________________________
    """)

    # Stores the time for output.
    query_time = df.counts_time.max()
    
    # Trains the model and prints the output. 
    lrm = sm.ols(formula="counts_truth ~  counts_authenticated", data=df).fit()
    print(lrm.summary())

    # Separately prints the model R-squared, P-values, confidence intervals and overall model significance. . 
    print("Model R-squared: ", lrm.rsquared)
    print("P-values:\n", lrm.pvalues)
    print("Confidence interval for model coefficients:\n", lrm.conf_int())    
    model_p = lrm.f_pvalue
    print("Overall model significance: ", model_p)

    # Creates a dataframe with the minimum and maximum values of counts_associated.
    df_minmax = pd.DataFrame({"counts_authenticated": [df.counts_associated.min(), df.counts_associated.max()]})

    # Makes predictions for those values.
    preds = lrm.predict(df_minmax)

    # Plots the observed data.  
    df.plot(kind="scatter", x="counts_authenticated", y="counts_truth")

    # Plots the least-squares line. 
    plt.plot(df_minmax, preds, c="red", linewidth=2)
    plt.savefig(lsplot_path, fmt="png", dpi=100)

    # Re-runs the regression using scikit-learn. 
    print("\nSCIKIT")    
    y = df["counts_truth"]
    X = np.array(df["counts_authenticated"].reshape(-1, 1))
    lrm = LinearRegression()    
    lrm.fit(X, y)

    # Prints the model R-squared. 
    rsquared = lrm.score(X, y)
    print("Model R-squared: ", rsquared)
    
    # Splits the dataset into 60% training and 40% testing. 
    df_train, df_test = train_test_split(df, test_size = 0.4, random_state = 5)

    # Trains model on the training set.
    y_train = df_train["counts_truth"]
    X_train = np.array(df_train["counts_authenticated"].reshape(-1, 1))    
    lrm_train = LinearRegression()
    lrm_train.fit(X_train, y_train)
    
    # Tests model on the test set. 
    y_test = df_test["counts_truth"]
    X_test = np.array(df_test["counts_authenticated"].reshape(-1, 1))    
    # Prints mean-squared error (MSE).  
    print("Residual sum of squares: %.2f" % np.mean((lrm_train.predict(X_test) - y_test) ** 2))
    # Prints explained variance score (1 is perfect prediction). 
    vscore = lrm_train.score(X_test, y_test)
    print('Variance score (1 = perfect prediction): %.2f' % vscore)

    # Plots outputs.
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, lrm_train.predict(X_test), color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.savefig(predplot_path, fmt="png", dpi=100)

    return [rsquared, model_p, vscore, query_time]

    
def ols_bin(df, lsplot_path, predplot_path):
    """
    Fits a simple OLS model on percentage ground truth and tests it on the 
    data, binning predictions to the nearest category. 
    Arguments: dataframe, file path to save the least-squares plot, file path to
    save predictions plot.     
    Returns a list containing the model R-squared, the overall model significance, 
    the accuracy score and the query time. 
    """

    print("""
    LINEAR MODEL, BINNING PREDICTIONS TO THE NEAREST CATEGORY
    ___________________________________
    """)

    # Stores the time for output.
    query_time = df.counts_time.max()    

    # Trains a linear model using the percentage count.
    lrm = sm.ols(formula="counts_truth_percent ~  counts_associated", data=df).fit()
    print(lrm.summary())

    # Separately prints the model R-squared, P-values, confidence intervals and overall model significance. . 
    print("Model R-squared: ", lrm.rsquared)
    print("P-values:\n", lrm.pvalues)
    print("Confidence interval for model coefficients:\n", lrm.conf_int())    
    model_p = lrm.f_pvalue
    print("Overall model significance: ", model_p)    

    # Creates a dataframe with the minimum and maximum values of counts_associated.
    df_minmax = pd.DataFrame({"counts_associated": [df.counts_associated.min(), df.counts_associated.max()]})

    # Makes predictions for those values.
    preds = lrm.predict(df_minmax)

    # Plots the observed data.  
    df.plot(kind="scatter", x="counts_associated", y="counts_truth")

    # Plots the least-squares line. 
    plt.plot(df_minmax, preds, c="red", linewidth=2)
    plt.savefig(lsplot_path, fmt="png", dpi=100)

    # Re-runs the regression using scikit-learn. 
    print("\nSCIKIT")    
    y = df["counts_truth_percent"]
    X = np.array(df["counts_associated"].reshape(-1, 1))
    lrm = LinearRegression()    
    lrm.fit(X, y)

    # Prints the model R-squared. 
    rsquared = lrm.score(X, y)
    print("Model R-squared: ", rsquared)

    # Splits the dataset into 60% training and 40% testing. 
    df_train, df_test = train_test_split(df, test_size = 0.4, random_state = 5)

    # Trains model on the training set.
    y_train = df_train["counts_truth"]
    X_train = np.array(df_train["counts_associated"].reshape(-1, 1))    
    lrm_train = LinearRegression()
    lrm_train.fit(X_train, y_train)
    
    # Tests model on the test set. 
    y_test = df_test["counts_truth_percent"]
    X_test = np.array(df_test["counts_associated"].reshape(-1, 1))    

    # Prints mean-squared error (MSE).  
    print("Residual sum of squares: %.2f" % np.mean((lrm_train.predict(X_test) - y_test) ** 2))
    
    # Predicts y values and rounds them to the nearest 25. 
    predicted = lrm_train.predict(X_test)    
    for i in range(len(predicted)):
        predicted[i] = int(25 * round(float(predicted[i])/25))
    predicted = predicted.astype(int)

    # Prints accuracy score (1 is perfect prediction).     
    ascore = metrics.accuracy_score(y_test, predicted)
    print('Accuracy score (1 = perfect prediction): %.2f' % ascore)

    # Plots outputs.
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, lrm_train.predict(X_test), color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.savefig(predplot_path, fmt="png", dpi=100)

    return [rsquared, model_p, ascore, query_time]
    
def logit(df, predplot_path):
    """
    Fits a logistic model on percentage ground truth and tests it on the data. 
    Arguments: dataframe, file path to save predictions plot.     
    Returns a list containing the model pseudo R-squared, the accuracy score
    and the query time.     
    """
    
    print("""
    LOGISTIC MODEL 
    ___________________________________
    """)

    # Stores the time for output.
    query_time = df.counts_time.max()    
    
    # Trains a logit model using the percentage count. Prints the coefficients and their significance levels. 
    y = df["counts_truth_percent"]
    X = df["counts_associated"]
    log = sm.MNLogit(y, X).fit()
    print(log.summary())

    # Separately prints the model pseudo R-squared, P-value and confidence intervals. 
    print("Model pseudo R-squared: ", log.prsquared)
    print("P-values:\n", log.pvalues)

    # Re-runs the regression using scikit-learn. 
    print("\nSCIKIT")    
    y = df["counts_truth_percent"]
    X = np.array(df["counts_associated"].reshape(-1, 1))
    log = LogisticRegression()    
    log.fit(X, y)

    # Prints the model R-squared. 
    pseudo_r = log.score(X, y)
    print("Model score: ", pseudo_r)
    
    # Splits the dataset into 60% training and 40% testing. 
    df_train, df_test = train_test_split(df, test_size = 0.4, random_state = 5)

    # Trains model on the training set.
    y_train = df_train["counts_truth_percent"]
    X_train = np.array(df_train["counts_associated"].reshape(-1, 1))    
    log_train = LogisticRegression()    
    log_train.fit(X_train, y_train)
    
    # Tests model on the test set. 
    y_test = df_test["counts_truth_percent"]
    X_test = np.array(df_test["counts_associated"].reshape(-1, 1))  
    predicted = log_train.predict(X_test)
    probs = log_train.predict_proba(X_test)
    
    # Prints accuracy score, confusion matrix, classification report and MSE. 
    ascore = metrics.accuracy_score(y_test, predicted)
    print("Accuracy score (1 = perfect prediction) ", ascore)
    print("Confusion matrix:\n", metrics.confusion_matrix(y_test, predicted))
    print("Residual sum of squares: %.2f" % np.mean((log_train.predict(X_test) - y_test) ** 2))

    # Plots outputs.
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, log_train.predict(X_test), color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.savefig(predplot_path, fmt="png", dpi=100)

    return [pseudo_r, 0, ascore, query_time]

def ordlogit(df):
    """
    Fits a proportional odds (ordinal) logistic model using R. 
    Arguments: dataframe. 
    """

    from rpy2.robjects.packages import importr
    import rpy2.robjects as ro

    print("""
    ORDINAL LOGISTIC MODEL 
    ___________________________________
    """)

    # Loads R packages. 
    base = importr('base')
    mass = importr('MASS')
    caTools = importr('caTools')
    
    # Converts df to an R dataframe. 
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()
    ro.globalenv["rdf"] = pandas2ri.py2ri(df) 

    # Makes R recognise counts_truth_percent as a factor. 
    ro.r("""rdf$counts_truth_percent <- as.factor(rdf$counts_truth_percent)""")

    # Fits an ordinal logistic regression in R. 
    formula = "counts_truth_percent ~ counts_associated"    
    ordlog = mass.polr(formula, data=base.as_symbol("rdf"))
    ro.globalenv["ordlog"] = ordlog
    print(base.summary(ordlog))

    # Performs a Chi-Square goodness-of-fit test.
    ordlog_chisq = ro.r("1-pchisq(deviance(ordlog),df.residual(ordlog))")
    print("Chi-square (want P > 0.05):", ordlog_chisq[0])

    """
    # Takes a sample of dataframe rows and splits it into a training and test set. 
    ro.r("bound <- floor((nrow(rdf)/4)*3)")
    ro.r("rdf <- rdf[sample(nrow(rdf)), ]")
    ro.r("rdf.train <- rdf[1:bound, ]")
    ro.r("rdf.test <- rdf[(bound+1):nrow(rdf), ]")

    # Takes a sample of dataframe rows and splits it into a training and test set. 
    ro.r("sample = sample.split(rdf$anycolumn, SplitRatio = .4)")
    ro.r("train = subset(data, sample == TRUE)")
    ro.r("test = subset(data, sample == FALSE)")
    """

def binary_model():
    """
    Specifies a binary logistic model which aims simply to determine whether or not the room is occupied. 
    """
    pass



