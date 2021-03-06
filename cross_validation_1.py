# -*- coding: utf-8 -*-
"""Cross_Validation_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZhlqyYpbPfkayZbj6uPOwl6vdX6m-U9c
"""

import pandas as pd
dataset = pd.read_csv('Churn_Modelling.csv')  
X = dataset.iloc[:, 3: 13].values
y = dataset.iloc[:, 13].values

from sklearn.preprocessing import LabelEncoder
labelencoder_X_1 = LabelEncoder() #instantiate an object of the class LabelEncoder
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1]) #ordinal encoding for column 1

labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2]) #ordinal encoding for column 2

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
ct = ColumnTransformer( #'encoder' is the name of the column transformer
    [('encoder', OneHotEncoder(), [1])],    # The column numbers to be transformed (here is [1] but can be [0, 1, 3])
    remainder='passthrough'                         # Leave the rest of the columns untouched
)
X = np.array(ct.fit_transform(X), dtype=np.float)

X = X[:, 1:]

'''from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2, random_state = 10) # We use random_state to make sure splitting contains the same data each time.
'''

#Standardise the data (x_standardised = (x - x_mean)/std_dev)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
'''X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test) #note that we use the scale set from the training set to transform the test set'''
X = sc.fit_transform(X)

import tensorflow as tf

def create_model():
  model = tf.keras.models.Sequential()

  #add input layer and first hidden layer
  model.add(tf.keras.layers.Dense(units=6, kernel_initializer='uniform', activation='relu'))

  #add 2nd hidden layer
  model.add(tf.keras.layers.Dense(units=6, kernel_initializer='uniform', activation='relu'))

  #output layer
  model.add(tf.keras.layers.Dense(units=1, kernel_initializer='uniform', activation='sigmoid')) #Sigmoid for binary, Softmax for multiclass
  
  model.compile(optimizer = 'adam', loss ='binary_crossentropy', metrics = ['accuracy'])
  
  return model

from sklearn.model_selection import KFold

n_split = 4

for train_index,test_index in KFold(n_split).split(X):
  x_train, x_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]
  
  model = create_model()
  model.fit(x_train, y_train, epochs=20, verbose=0)
  
  print('Model evaluation ', model.evaluate(x_test,y_test))

