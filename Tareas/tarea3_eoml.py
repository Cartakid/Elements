# -*- coding: utf-8 -*-
"""Tarea3 Juan Jose-EoML-UFM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14aVzfflMgKbdckuyEjuzGt07TuK_Sq96

# Problemas conceptuales

1.   Lee la sección 4.4.2 del libro Elements of Machine Learning. Trata sobre el uso de análisis de varianza en una base de datos de una enfermedad del corazón. Describe en qué consiste este análisis.
2.   Haz un resumen de la sección 4.5 del libro Introduction to Statistical Learning. Puedes describir las ventajas y desventajas de cada método de clasificación en un cuadro diagrama o en prosa. Además, describe los seis escenarios mostrados en la lectura y sintetiza cuáles fueron las razones por las que cada método fue mejor o peor que otros.
3.   Problema 7 del capítulo 4

Se analizaron los factores que pueden causar un paro cardiaco. Se escogieron hombres entre 15-64 años porque han de ser los más comunes en tener alguna enfermedad cardiovascular. Hay 160 casos y 302 muestras de control, y siete variables (Edad, consumo de alcohol, obesidad, antecedentes con enfermedad cardiovascular, LDL, consumo de tabaco y la presión) para luego identicar las que más relación tienen con la hipotesis. Con el coeficiente de varianza se clasifica que tabaco, LDL, antecedentes y la edad tienen una relacion con el ataque cardiaco.

**Regresión logística**
 Se estima la media y varianza en las suposiciones de Gauss.

**LDA** hace más restricciones en las suposiciones de Gauss, por lo cual hace un mejor trabajo que los modelos logísticos.

**QDA** sirve como un compromiso entre los no-parametricos KNN, LDA y LR. Debido a que es cuadrática tiene más rango que los métodos lineales. 

**K-cercanos vecinos** no hay suposiciones del límite decisivo. Cuando no es lineal la data, está es la mejor opción pero no indica que predictores son importantes. 

**Escenario 1** LDA es mejor porque no utiliza límites lineales en las 2 clases de 20 observaciones de prueba. KNN no funciona por la varianza, QDA por la flexibilidad que usa y LR utiliza un límite lineal innecesario.

**Escenario 2** Mismo escenario 1 excepto con una correlación de -0.5, por lo cual los rendimientos de los métodos son parecidos al del escenario 1.

**Escenario 3** X1 y X2 de distribución-t con 50 observaciones por clase. Parecido a una distribución normal pero con más observaciones en las colas. Se utiliza LR porque LDA viola las suposiciones lineales y no es una distribución normal. QDA no sirve porque es no-normal.

**Escenario 4** Distribución normal con una correlación de 0.5 entre los predictores de la primera clase y -0.5 de la segunda. Se utiliza QDA porque corresponde a las suposiciones para utilizar este método.

**Escenario 5** Dentro de cada clase, las observaciones se generaron de una distribución normal sin correlación de los predictores. QDA es la mejor seguido por KNN por los límites cuadráticos.

**Escenario 6** Escenario 5 pero las respuestas son una muestra más compleja no lineal. KNN brinda el mejor resultado pero con diferentes factores se vuelve un mal método por la data que no es lineal ni cuadrática.
"""

import pandas as pd
import math

dividend=10
mean=0
variance=36
percentage_return=4
companies=0.8

prob=companies*math.exp(-1/(variance*2)*(percentage_return-dividend)*(percentage_return-dividend))/(companies*math.exp(-1/(variance*2)*(percentage_return-dividend)*(percentage_return-dividend))+(1-companies)*math.exp(-1/(variance*2)*(percentage_return-mean)*(percentage_return-mean)))
print("The probability of the company to issue dividend is:", prob)

"""# Problema aplicado

Utiliza la base de datos Auto en http://www-bcf.usc.edu/~gareth/ISL/data.html para predecir si un carro tiene alto o bajo consumo de gasolina.


1.   Crea una variable binaria mpg01 que contiene 1 si mpg tiene un valor mayor a la mediana y 0 si tiene un valor menor a la mediana. Haz un nuevo dataset con esta columna y otras variables importantes del dataset original de auto.
2.   Usa representaciones gráficas como gráficas de dispersión y diagramas de cajas para investigar qué otras variables están asociadas a mpg01.
3.   Separa los datos en de entrenamiento y de prueba.
4.   Queremos predecir mpg01. Utiliza las variables que según tu análisis en b) estaban más asociadas como predictores. Harás más de cuatro modelos, uno con LDA, luego QDA, luego regresión logística y por último KNN (con diferentes valores de k).
5.   Calcula el error de prueba de cada modelo y compáralos. Qué método de clasificación es tu preferido? Argumenta tu respuesta como si fuera un escenario de la sección 4.5 del libro
"""

#Upload file
from google.colab import files
uploaded = files.upload()
import pandas as pd
import io
auto= pd.read_csv(io.BytesIO(uploaded['Auto.csv']))

#1         Crear variable mpg01
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import statsmodels
import statsmodels.formula.api as smf

cars=pd.DataFrame(data=auto)
df=cars
df['mpg01'] = np.where(df['mpg']>df['mpg'].mean(), '1', '0')

#2         Plots
plt.scatter(x="cylinders", y="mpg01", data=df)

sns.boxplot(x="mpg01", y="displacement", data=df)

plt.scatter(x="horsepower", y="mpg01", data=df)

sns.boxplot(x="mpg01", y="weight", data=df)

plt.scatter(x="acceleration", y="mpg01", data=df)

sns.boxplot(x="mpg01", y="year", data=df)

plt.scatter(x="origin", y="mpg01", data=df)

corr = df.corr()

# plot the heatmap
sns.heatmap(corr)

#3        Train & test

import sklearn
df_train = df[df["year"]<77]
df_test = df[df["year"]>77] 
ytrain = pd.factorize(df_train["mpg01"])[0]
ytest = pd.factorize(df_test["mpg01"])[0]
xtrain = df_train[df.columns[1:3]]
xtest = df_test[df.columns[1:3]]

#4 Predecir variables

#LR

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
  
lr = LogisticRegression()
lr.fit(xtrain, ytrain)
ypred = lr.predict(xtest)
confusion_matrix(ytest, ypred)
accuracy_score(ytest, ypred)

#QDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

qda= QuadraticDiscriminantAnalysis()
qda.fit(xtrain, ytrain)
ypred = qda.predict(xtest)
ypred[0:5]
confusion_matrix(ytest, ypred)
accuracy_score(ytest, ypred)

#LDA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


lda = LinearDiscriminantAnalysis()
lda.fit(xtrain, ytrain)
ypred = lda.predict(xtest)
ypred[0:5]
confusion_matrix(ytest, ypred)
accuracy_score(ytest, ypred)

#KNN
from sklearn.neighbors import KNeighborsClassifier

k_near = KNeighborsClassifier()
k_near.fit(xtrain, ytrain)
ypred = k_near.predict(xtest)
confusion_matrix(ytest, ypred)
accuracy_score(ytest, ypred)

"""LDA porque tiene menos error para la prueba mientras que los demás tiene más probabilidad de error."""