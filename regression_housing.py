# -*- coding: utf-8 -*-
"""Regression_housing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CD4hqrrXkFcFm5jekwl_IXtjF_-jfhGm
"""

import pandas as pd

from sklearn.datasets import load_boston
boston_dataset = load_boston()  #selling price of a given house in the Boston (MA) area
boston_dataset

print('data is : {}'.format(boston_dataset.data))
print('independent variable names are : {}'.format(boston_dataset.feature_names))
print('labels or prices : {}'.format(boston_dataset.target))

df = pd.DataFrame(boston_dataset.data, columns=boston_dataset.feature_names)
df['Price'] = boston_dataset.target
df.head(n=10)   #show the first 10 rows of data

#Use the describe() method to understand the data
df.describe(include='all')

"""Architecture based on two Dense layers, the first with 128 and the second with 64 neurons, both using a ReLU (Rectified Linear Unit) activation function. A dense layer with a linear activation will be used as output layer."""

#Create train and test databases
from sklearn.model_selection import train_test_split

X = df.loc[:, df.columns != 'Price']
y = df.loc[:, df.columns == 'Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

#Standardization
mean = X_train.mean(axis=0)
std = X_train.std(axis=0)
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

from keras.models import Sequential
from keras.layers import Dense
model = Sequential()
model.add(Dense(128, input_shape=(13, ), activation='relu', name='dense_layer_1'))
model.add(Dense(64, activation='relu', name='dense_layer_2'))
model.add(Dense(1, activation='linear', name='dense_output'))
model.compile(optimizer='adam', loss='mse')
model.summary()

#Train
model.fit(X_train, y_train, epochs=100)

#Model evaluation
loss = model.evaluate(X_test, y_test)
print('Mean squared error on test data: ', loss)

#Note : there is no correct MSE. It is used to select one model over another.