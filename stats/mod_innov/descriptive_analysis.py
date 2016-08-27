# Romain Ducarrouge

import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats

dataframe = pd.read_csv("data/rssi/finalData1_HeadCount.csv")
dataframe = dataframe.drop("Unnamed: 0", axis=1)

''' DESCRIPTIVE STATS '''
# Plotting Head Count changes over time
Count_Bar = sns.barplot(x="hour", y="Nb_People", data=dataframe)
Count_Bar.figure.savefig("data/rssi/graphs/HeadCount_bar_chart.png")

# Plotting RSSI Level changes over time
Rssi_Bar =  sns.barplot(x="hour", y="rssi", data=dataframe)
Rssi_Bar.figure.savefig("data/rssi/graphs/RSSI_bar_chart.png")


rssi_vs_count = sns.lmplot('Nb_People', 'rssi', data=dataframe, fit_reg=True)
rssi_vs_count.savefig("data/rssi/graphs/RSSI_vs_HeadCount_scatter_plot.png")

print("Raw Data:")
print(dataframe.describe())

RssiCount = dataframe[['rssi','Nb_People']]
print("\n", RssiCount.corr())


# Removing outliers
print("\nData after removing Outliers:")

#no_outliers = dataframe[(np.abs(stats.zscore(dataframe)) < 3).all(axis=1)]
#no_outliers = dataframe[(np.abs(dataframe['rssi','Nb_People'])>3).any(1)]
#print(no_outliers.head(3))