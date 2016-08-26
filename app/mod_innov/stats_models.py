# Romain Ducarrouge

import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import seaborn as sns

dataframe = pd.read_csv("data/rssi/formattedData.csv") 		# includes rssi1 data
dataframe = dataframe.drop(['Unnamed: 0','date'], axis=1)

rssi2 = pd.read_csv("data/rssi/RSSI_data_merged.csv")		# uses rssi2 data
rssi2['hour'] = rssi2['time'].map(lambda x: x[:2])
rssi2['min'] = rssi2['time'].map(lambda x: x[-2:])
rssi2 = rssi2.drop(['Unnamed: 0','year','date','month','time'], axis=1)

frames = [dataframe, rssi2]
data = pd.concat(frames, axis=1, join='outer')
data = data.drop('rssi_1', axis=1)

#print(data.head())
model_name = []
models_Rsquared = []

def lm_uni_rssi(data):			# Linear Model for People and rssi
	name = 'People~rssi'
	lm = sm.ols(formula="Nb_People ~ rssi", data=data).fit()
	# Print the model weights/parameters
	print(lm.params)
	print(lm.summary())
	models_Rsquared.append(lm.rsquared)
	model_name.append(name)
	
	lm_plot = sns.lmplot('Nb_People', 'rssi', data=data, fit_reg=True)
	lm_plot.savefig("data/rssi/graphs/LM_" + name +"_model_plot.png")


def lm_uni_rssi2(data):			# Linear Model for People and rssi2
	name = 'People~rssi_2'
	lm = sm.ols(formula="Nb_People ~ rssi_2", data=data).fit()
	print(lm.params)
	print(lm.summary())
	models_Rsquared.append(lm.rsquared)
	model_name.append(name)
	
	lm_plot = sns.lmplot('Nb_People', 'rssi_2', data=data, fit_reg=True)
	lm_plot.savefig("data/rssi/graphs/LM_" + name +"_model_plot.png")


def lm_uni_diff(data):			# Linear Model for People and difference of rssi and rssi2
	name = 'People~Difference(rssi1-rssi2)'
	lm = sm.ols(formula="Nb_People ~  difference", data=data).fit()
	print(lm.params)
	print(lm.summary())
	models_Rsquared.append(lm.rsquared)
	model_name.append(name)
	
	lm_plot = sns.lmplot('Nb_People', 'difference', data=data, fit_reg=True)
	lm_plot.savefig("data/rssi/graphs/LM_" + name +"_model_plot.png")

	
def lm_multi_rssi_hour(data):				# Linear Model for People and rssi+hour
	name = 'People~rssi+hour'
	lm2 = sm.ols(formula="Nb_People ~  rssi + hour", data=dataframe).fit()
	print(lm2.params)
	print(lm2.summary())
	models_Rsquared.append(lm2.rsquared)
	model_name.append(name)

	
def lm_multi_rssi_min(data):				# Linear Model for People and rssi+min
	name = 'People~rssi+min'
	lm3 = sm.ols(formula="Nb_People ~  rssi + min", data=dataframe).fit()
	print(lm3.params)	
	print(lm3.summary())
	models_Rsquared.append(lm3.rsquared)
	model_name.append(name)

	
def lm_multi_rssi_hour_min(data):				# Linear Model for People and rssi+hour+min
	name = 'People~rssi+hour+min'
	lm4 = sm.ols(formula="Nb_People ~  rssi + hour + min", data=dataframe).fit()
	print(lm4.params)
	print(lm4.summary())
	models_Rsquared.append(lm4.rsquared)
	model_name.append(name)


''' Looking into Naive Bayes '''
from statistics import mean
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split

def NaiveBayes_rssi1_NbPeople(dataframe):			# using Rssi reading from Mark's laptop
	X = dataframe[['Nb_People']]
	Y = dataframe[['rssi']]
	model = GaussianNB()		# Fit a Naive Bayes model to the data
	Naive_models_scores = []

	i=0
	for i in range(0, 100):		# run i times (due to random dataset split)
		# Split the data into Train and Test sets
		X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, train_size=0.8)
		model.fit(X_train,Y_train) 		# Fit the training model
		predicted = model.predict(X_test)
		expected = Y_test

		acc_score = metrics.accuracy_score(expected, predicted)
		Naive_models_scores.append(acc_score)
		i += 1

	score = mean(Naive_models_scores)
	name = "NaiveBayesModel1"

	print("On average the Naive Bayes model using RSSI_1 has the following score: " + str(score))
	models_Rsquared.append(score)
	model_name.append(name)
	
	
def NaiveBayes_rssi2_NbPeople(dataframe, rssi2):	# using Rssi reading from Luke's laptop	
	X = dataframe[['Nb_People']]
	Y = rssi2[['rssi_2']]
	model = GaussianNB()		# Fit a Naive Bayes model to the data
	Naive_models_scores = []

	i=0
	for i in range(0, 100):		# run i times (due to random dataset split)
		# Split the data into Train and Test sets
		X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, train_size=0.8)
		model.fit(X_train,Y_train) 		# Fit the training model
		predicted = model.predict(X_test)
		expected = Y_test

		acc_score = metrics.accuracy_score(expected, predicted)
		Naive_models_scores.append(acc_score)
		i += 1

	score = mean(Naive_models_scores)
	name = "NaiveBayesModel2"

	print("On average the Naive Bayes model using RSSI_2 has the following score: " + str(score))
	models_Rsquared.append(score)
	model_name.append(name)

print(data.head())

lm_uni_rssi(data)
lm_uni_rssi2(data)
lm_uni_diff(data)
lm_multi_rssi_hour(data)
lm_multi_rssi_min(data)
lm_multi_rssi_hour_min(data)

NaiveBayes_rssi1_NbPeople(dataframe)
NaiveBayes_rssi2_NbPeople(dataframe, rssi2)

print('\n')
i=0
for i in range(0, len(model_name)):
	print(str(models_Rsquared[i]) + '\t ' + model_name[i],)
	i +=1
	
best_model = max(models_Rsquared)
a = models_Rsquared.index(best_model)
print("\nThe best model is: '", model_name[a], "' with R Squared: ", models_Rsquared[a])

