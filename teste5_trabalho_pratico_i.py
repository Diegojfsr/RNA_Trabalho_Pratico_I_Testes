# -*- coding: utf-8 -*-
"""Teste5 - Trabalho Pratico I

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xN3R8RrRf8mc5Xr1Xif0iaQyml9unaus
"""

#import libraries 

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

#dados de aprendizagem
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/train.csv?raw=true'
train = pd.read_csv(url)

# remove linhas contendo nan
train.dropna(inplace=True)

# dados de teste
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/test.csv?raw=true'
test = pd.read_csv(url)

# Dados de envio
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/sample_submission.csv?raw=true'
sample_submission = pd.read_csv(url)


print(len(train), len(test))

#integração de dados

# Conecte dois dados csv para corresponder ao número de colunas de dados de aprendizado e dados de teste (se o número de colunas não for o mesmo, a entrada não será aprovada (exceto para dados enviados)

data = pd.concat([train, test], sort=False)
data.tail(10)

#Engenharia de recursos


data['HomePlanet'].replace(['Earth','Europa', 'Mars'], [0, 1, 2], inplace=True)
data['Destination'].replace(['TRAPPIST-1e', '55 Cancri e', 'PSO J318.5-22'], [0, 1, 2], inplace=True)
data['Transported'].replace([False, True], [0, 1], inplace=True)
data['CryoSleep'].replace([False, True], [0, 1], inplace=True)
data['VIP'].replace([False, True], [0, 1], inplace=True)

# Separe os dados na coluna Cabine com "/" e adicione as colunas "deck", "num" e "side" e atribua as informações separadas
data[['deck', 'num','side']] = data['Cabin'].str.split('/', expand=True)

# Remova colunas de cabine obsoletas
data = data.drop(['Cabin'], axis=1)

# substitui os dados no deck e nas colunas laterais por inteiros
data['deck'] = data['deck'].replace({'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'T':7})
data['side'] = data['side'].replace({'P':0, 'S':1})

data.head()

## dividido em colunas de sobrenome

data['Name'] = data['Name'].str.split(' ').str[1]
Names = data['Name'].tolist()

NameValues = []
for name in Names:
    if type(name) is str:
        NameValues.append(Names.count(name)/len(Names))
    else:
        NameValues.append(0)

data['Name'].replace(Names, NameValues, inplace=True)
data.head()

data['PassengerId'] = data['PassengerId'].str.split('_').str[1]

# Converte os dados da coluna inteira para o tipo float

data = data.astype('float')
data.info()

# Preencha os valores ausentes com o valor mais frequente

data = data.fillna(data.mean())
data.head(10)

train = data[:len(train)]
test = data[len(train):]

Y_train = train['Transported']
X_train = train.drop('Transported', axis = 1)
X_test = test.drop('Transported', axis = 1)

# Importar TensorFlow e tf.keras

import tensorflow as tf
from tensorflow import keras

model = keras.Sequential()
model.add(keras.layers.Dense(16, input_dim=15, bias_initializer='zeros', activation='softsign'))
model.add(keras.layers.Dense(8, bias_initializer='zeros', activation='tanh'))
model.add(keras.layers.Dense(1, bias_initializer='zeros', activation='sigmoid'))

model.compile(optimizer='adam',
             loss='binary_crossentropy',
             metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=50)

# prever

y_pred = model.predict(X_test)
y_pred[:20]

def booling(n):
    if n >= 0.5:
        return True
    else:
        return False
sub = sample_submission
sub['Transported'] = [booling(i) for i in y_pred]
sub.to_csv("submission.csv", index=False)
sub.head(10)