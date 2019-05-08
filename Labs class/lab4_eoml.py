# -*- coding: utf-8 -*-
"""Laboratorio 4 Juan Jose- EoML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ooubSeHV8uF0lRh25-7bxyJc2ZodcuYJ

# Laboatorio 4

En este laboratorio usaremos cuatro tipo de clasificadores sobre datos de bolsa de valores para predecir si el mercado está de subida o de bajada para cierta fecha. Los datos están en https://github.com/JWarmenhoven/ISLR-python/blob/master/Notebooks/Data/Smarket.csv.
"""

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import statsmodels
import statsmodels.formula.api as smf

print("Todos los paquetes han sido importados:")
print("Numpy version: {}".format(np.__version__))
print("Pandas version: {}".format(pd.__version__))
print("Matplotlib version: {}".format(matplotlib.__version__))
print("Seaborn version: {}".format(sns.__version__))
print("Statsmodels-learn version: {}".format(statsmodels.__version__))

"""## Explorando los datos

Las variables en smarket son


*   Año
*   Lag1 a Lag5: porcentaje de retornos de los cinco días previos
*   Volume: el número de intercambios el día previo en billones
*   Today: porcentaje de retorno en ese día
*   Direction: si el mercado está de subida o bajada ese día
"""

url = 'https://raw.githubusercontent.com/JWarmenhoven/ISLR-python/master/Notebooks/Data/Smarket.csv'
smarket = pd.read_csv(url)
smarket = smarket.drop('Unnamed: 0', axis=1)

smarket.head()

smarket.describe()

"""Predeciremos direction, que esperamos que sea binario. Verifiquemos que lo es"""

sns.countplot(x='Direction',data=smarket, palette='hls')

"""Generamos una matriz de correlaciones entre variables para visualizar"""

#smarket.corr()

cols = list(smarket)
print(cols)

coefs = np.corrcoef(smarket[cols[0:8]].values.T)
heatMap = sns.heatmap(coefs, annot = True, yticklabels=cols[0:8], xticklabels=cols)

"""Noten que excluí la columna de Direction porque no es numérica. La única correlación que sobresale es entre volumen y años con 0.539006, las demás son menores a 0.05. Esto último era de esperarse: no parece haber correlacción entre los retornos de hoy y los de días anteriores. Generemos una función de gráfica de dispersión para visualizar la relación entre volumen y año."""

def make_scatter_plot(dataframe, input_feature, target,
                      slopes=[], biases=[], model_names=[]):
  """ Creates a scatter plot of input_feature vs target along with the models.
  
  Args:
    dataframe: the dataframe to visualize
    input_feature: the input feature to be used for the x-axis
    target: the target to be used for the y-axis
  """      
  # Define some colors to use that go from blue towards red
  colors = [cm.coolwarm(x) for x in np.linspace(0, 1, len(slopes))]
  
  # Generate the Scatter plot
  x = dataframe[input_feature]
  y = dataframe[target]
  plt.ylabel(target)
  plt.xlabel(input_feature)
  plt.scatter(x, y, color='black', label="")
  plt.show()

"""### Ejercicio

En el laboratorio utilizarás los métodos de clasificación: regresión logística, análisis de discriminante lineal, análisis de discriminante cuadrático y vecinos k-cercanos. Para smarket, cuál crees que será el mejor predictor o el más apropiado para la variable Direction? Los aspectos que debes tomar en cuenta son: número de observaciones, normalidad de la distribución de los datos, no linealidad entre la relación entre los predictores y el target. Responde en la celda de abajo

Años y volumen porque en las bolsas de valores los años son importantes por los sucesos historicos que afectan económicamente ese año. Volumen por las transacciones realizadas durante el año.

## Análisis (Tarea)

Para cada uno de los cuatro métodos de clasificación, escoge observaciones de entrenamiento y otras de prueba

1.   Genera un modelo de predicción para la variable Direction usando observaciones de entrenamiento
2.   Realiza cuadros de confusión para cada uno
"""

smarket_train = smarket[smarket["Year"] < 2005]
smarket_test = smarket[smarket["Year"] >= 2005]
ytrain = pd.factorize(smarket_train["Direction"])[0]
ytest = pd.factorize(smarket_test["Direction"])[0]
xtrain = smarket_train[smarket.columns[1:3]]
xtest = smarket_test[smarket.columns[1:3]]

"""### Regresión logística"""

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()
lr.fit(xtrain, ytrain)
ypred = lr.predict(xtest)
confusion_matrix(ytest, ypred)

accuracy_score(ytest, ypred)

"""### Análisis de discriminante lineal"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


lda = LinearDiscriminantAnalysis()
lda.fit(xtrain, ytrain)
ypred = lda.predict(xtest)
ypred[0:5]

confusion_matrix(ytest, ypred)

accuracy_score(ytest, ypred)

"""### Análisis de discriminante cuadrático"""

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

qda= QuadraticDiscriminantAnalysis()
qda.fit(xtrain, ytrain)
ypred = qda.predict(xtest)
ypred[0:5]

confusion_matrix(ytest, ypred)

accuracy_score(ytest, ypred)

"""### Vecinos k-cercanos"""

from sklearn.neighbors import KNeighborsClassifier

k_near = KNeighborsClassifier()
k_near.fit(xtrain, ytrain)
ypred = k_near.predict(xtest)
confusion_matrix(ytest, ypred)

accuracy_score(ytest, ypred)