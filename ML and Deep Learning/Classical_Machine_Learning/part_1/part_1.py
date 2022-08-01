# This set of code helps in loading, processing and visualisation of the Wisconsin Breast Cancer data set
# The data set is imported in the form pf a csv extension file
#importing libraries for data load and simple tabular view
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 100)
cancer_data= pd.read_csv('data.csv',  index_col= None, na_values='?')
print(cancer_data.head(6))
print("The shape of the original data is: ", cancer_data.shape)


#Dropping the unnecessary columns
cancer_data.drop('Unnamed: 32', axis=1 , inplace=True)
cancer_data.drop('id', axis=1 , inplace=True)
print("Shape of data after dropping the unwanted columns: ", cancer_data.shape)
# checking missing data
print(cancer_data.isnull().sum())
# value count of 2 classes
print("Value count of 2 classes are: \n", cancer_data["diagnosis"].value_counts())          
# full information of dataset
print(cancer_data.info())


#libraries for plotting
import time
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import hypertools as hyp


# data duplication check
cancer_data.duplicated

print('Number of rows before discarding duplicates = %d' % (cancer_data.shape[0]))
data2 = cancer_data.drop_duplicates()
print('Number of rows after discarding duplicates = %d' % (data2.shape[0]))

#Separate the predictors and target.
x = cancer_data.loc[: , 'radius_mean':'fractal_dimension_worst']
y_true = cancer_data.loc[:, 'diagnosis']
print("Shape of x: ", x.shape)
print("Shape of y_true: ", y_true.shape)


#Visualisation


sns.set(style="whitegrid")
ax = sns.countplot(x = y_true)       # M = 212, B = 357
B, M = y_true.value_counts(sort=True) 
plt.show()


#1.1 Violin Plot
# first ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,0:10]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90)
plt.show()

#1.2 Violin Plot
# second ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,10:20]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90)
plt.show()

#1.3 Violin Plot
# last ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,20:31]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90)
plt.show()

#2.1 Box Plot
# first ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,0:10]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.boxplot(x="features", y="value", hue="diagnosis", data=data)
plt.xticks(rotation=90)
plt.show()

#2.2 Box Plot
# second ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,10:20]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.boxplot(x="features", y="value", hue="diagnosis", data=data)
plt.xticks(rotation=90)
plt.show()

#2.3 Box Plot
# last ten features
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,20:31]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.boxplot(x="features", y="value", hue="diagnosis", data=data)
plt.xticks(rotation=90)
plt.show()

#3.1 Swarm Plot
# first ten features
sns.set(style="whitegrid", palette="muted")
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,0:10]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
tic = time.time()
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)

plt.xticks(rotation=90)
plt.show()

#3.2 Swarm Plot
# second ten features
sns.set(style="whitegrid", palette="muted")
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,10:20]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
tic = time.time()
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)

plt.xticks(rotation=90)
plt.show()

#3.3 Swarm Plot
# last ten features
sns.set(style="whitegrid", palette="muted")
data_dia = y_true
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y_true,data_n_2.iloc[:,20:31]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
tic = time.time()
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)

plt.xticks(rotation=90)
plt.show()

print("PART 1 of Assignment is Complete")
print("Data loading is again followed in Part 2 and Part 3 of the assignment")
