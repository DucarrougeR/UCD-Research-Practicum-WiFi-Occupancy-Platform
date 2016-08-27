# Romain Ducarrouge

''' Comparing the RSSI obsverations from table locations '''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# data_1 is observation file from Mark's laptop at table ~7
data_1 = pd.read_csv("data/rssi/RSSI_data1.csv")

# data_2 is observation file from Luke's laptop at table 3
data_2 = pd.read_csv("data/rssi/RSSI_data2.csv")

# Test to ensure data is not entirely the same
#(data_1 != data_2).all(1)

# Make dataframes start and end times match
data_1 = data_1.drop([0])		# drop first row (11:56:13)
data_2 = data_2.drop([170])		# drop last row (13:22:00)

# Modify field for merging later
data_1['time'] = data_1['time'].map(lambda x: x[:-3])
data_2['time'] = data_2['time'].map(lambda x: x[:-3])

# Keep one observation per minute
data_1 = data_1.drop_duplicates('time', keep='last')
data_2 = data_2.drop_duplicates('time', keep='last')

# Resetting index for merging dataframes
data_1 = data_1.reset_index()
data_2 = data_2.reset_index()
 
# Merged Dataframe
compare_df = pd.merge(data_1, data_2, on=['time','date','month','year'], how='outer')

# Cleaning dataframes (duplicate or non relevant columns)
compare_df = compare_df.drop(['index_x','index_y'], axis=1)
compare_df = compare_df.rename(columns={'rssi_x': 'rssi_1', 'rssi_y': 'rssi_2'})


sns.lmplot('rssi_1', 'rssi_2',
           data=compare_df,
           fit_reg=True)
plt.title('Rssi_1 vs Rssi_2')
plt.xlabel('rssi_1')
plt.ylabel('rssi_2')

plt.savefig("data/rssi/graphs/Comparing_RSSI_scatter_plot.png")

compare_df['difference'] = abs(compare_df['rssi_1']-compare_df['rssi_2'])

# Comparing distributions
compare_df[["rssi_1","rssi_2"]].hist(figsize=(20, 8), bins=30, color='red')
plt.savefig("data/rssi/graphs/RSSI_1and2_histogram.png")

compare_df.to_csv("data/rssi/RSSI_data_merged.csv")

print("complete")

