# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 01:58:24 2020

@author: Nilendu Saha

The code deals with the training and prediction of the Yaw angle values using Deep Learning method. 
"""


import pandas
import matplotlib.pyplot as plt

import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense,Dropout


#%% Load datasets
dataset = pandas.read_excel(r'yaw.xlsx')
plt.plot(dataset)
plt.show()
#%% Creating Random Noise
noise = numpy.random.normal(0, .05, dataset.shape)
tst_data_noise = numpy.random.normal(0, .005, dataset.shape)

dataset_noise = dataset + noise
#%% Creating another noisy test dataset
test_dataset_noise = dataset + tst_data_noise
print(dataset_noise)
plt.plot(dataset_noise)
plt.show()
plt.plot(test_dataset_noise)
plt.show()
#%% Normalize

# Normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset_noise = scaler.fit_transform(dataset_noise)
dataset = scaler.fit_transform(dataset)
test_dataset_noise = scaler.fit_transform(test_dataset_noise)
print("Normalized Dataset\n")
print(dataset_noise)
print(dataset)
plt.plot(dataset)
plt.show()

#%%Setting the input and ground truth
X = dataset_noise
y = dataset
#%% Model Design
model = Sequential()
model.add(Dense(100, input_dim=X.shape[1], activation='tanh'))
model.add(Dense(50, activation='tanh'))
model.add(Dropout(0.1))
model.add(Dense(25, activation='tanh'))
model.add(Dense(1))

#%%Training the model
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(X,y,verbose=1,batch_size=len(X),epochs=100, validation_data=(test_dataset_noise,dataset))

#%% Model Prediction
prediction = model.predict(test_dataset_noise)

print("Actual")
print(y[0:5])

print("Prediction")
print(prediction[0:5])

#%% training and validation loss

loss_train = history.history['loss']
loss_val = history.history['val_loss']
epochs = range(1,101)
plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.plot(epochs, loss_val, 'b', label='validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

#%%

# Prediction Graph Function
def prediction_graph(pred, y, sort=True):
    t = pandas.DataFrame({'pred': pred, 'y': y.flatten()})
    if sort:
        t.sort_values(by=['y'], inplace=True)
    plt.plot(t['pred'].tolist(), label='predicted angles')
    plt.plot(t['y'].tolist(), label='expected angles')
    plt.ylabel('Yaw Angle')
    plt.xlabel('Time Frame')
    plt.legend()
    plt.show()
    
#%% Graph Prediction
prediction_graph(prediction.flatten(),y,sort=False)

#%% Prediction values should be inversed for making the comparison graph in the next code.

invPredict = scaler.inverse_transform(prediction)
