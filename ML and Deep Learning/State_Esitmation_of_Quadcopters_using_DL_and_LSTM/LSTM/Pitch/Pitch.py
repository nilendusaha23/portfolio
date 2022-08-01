# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 01:29:05 2020

@author: Nilendu Saha

The code deals with the training and prediction of the Pitch angle values using LSTM method. 
"""

import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.optimizers import SGD
from keras.optimizers import Adagrad
from keras.optimizers import RMSprop
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


# fix random seed for reproducibility
numpy.random.seed(7)

# load the dataset
dataset = pandas.read_excel('pitch.xlsx')
plt.plot(dataset)
plt.show()
print(dataset)

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
plt.plot(dataset)
plt.show()
# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

# reshape into X=t and Y=t+1
look_back = 3
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))
#%%
print(trainX.shape)
print(type(trainX))
#%%
# The stacked LSTM model
batch_size = 1
model = Sequential()
model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True, return_sequences=True))
model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))
model.add(Dense(1))


model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc'])
model.summary()

history = model.fit(trainX, trainY, epochs=20, batch_size=batch_size, verbose=1, shuffle=False, validation_data=(testX,testY))
#%%
loss_train = history.history['loss']
loss_val = history.history['val_loss']
epochs = range(1,21)
plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.plot(epochs, loss_val, 'b', label='validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
#%%
# make predictions
trainPredict = model.predict(trainX, batch_size=batch_size)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)

# invert predictions(de-normalizing)
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset), label='expected')
plt.plot(trainPredictPlot, label='train predictions')
plt.plot(testPredictPlot, label='test predictions')
plt.ylabel('Pitch Angle')
plt.xlabel('Time Frame')
plt.legend()
plt.show()

#%% Join both the test and train predictions

print(trainPredict)
print("\n")
print(testPredict)
print("JOINED\n")
arr = numpy.concatenate((trainPredict, testPredict))

print(arr)
print(arr.shape)

## convert your array into a dataframe
df2 = pandas.DataFrame(arr)

## save to xlsx file

filepath = r'pitch_pred_LSTM.xlsx'

df2.to_excel(filepath, index=False)
print("done")

#%% Predicting the future

x_input = numpy.array([0.001757289, 0.001742561, 0.001727954])
temp_input=list(x_input)
lst_output=[]
i=0
while(i<100):
    
    if(len(temp_input)>3):
        x_input=numpy.array(temp_input[1:])
        print("{}number input {}".format(i,x_input))
        #print(x_input)
        x_input = x_input.reshape((1, look_back, batch_size))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        print("{}number output {}".format(i,yhat))
        temp_input.append(yhat[0][0])
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.append(yhat[0][0])
        i=i+1
    else:
        x_input = x_input.reshape((1, look_back, batch_size))
        yhat = model.predict(x_input, verbose=0)
        print(yhat[0])
        temp_input.append(yhat[0][0])
        lst_output.append(yhat[0][0])
        i=i+1
    

print(lst_output)

#%% Plot future prediction

future_pred=numpy.arange(1,101)
plt.plot(future_pred,lst_output)