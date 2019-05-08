# -*- coding: utf-8 -*-
"""Laboratorio 2 Juan Jose.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yi4L9e36bWyNUzsnRS1lCCnXMR_qmJjg

# Laboatorio 2

En este laboratorio exploraremos otra de las bases de datos de juguete en `scikit-learn`. Primero importamos todos los módulos potencialmente útiles:
"""

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import patsy
from patsy import dmatrix

import sklearn
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

print("Todos los paquetes han sido importados:")
print("Numpy version: {}".format(np.__version__))
print("Pandas version: {}".format(pd.__version__))
print("Matplotlib version: {}".format(matplotlib.__version__))
print("Seaborn version: {}".format(sns.__version__))
print("patsy version: {}".format(patsy.__version__))
print("Scikit-learn version: {}".format(sklearn.__version__))

"""## Modificando los parámetros de seaborn

[Explora la documentación en seaborn](https://seaborn.pydata.org/tutorial/aesthetics.html) y escoge algún estilo de gráficas para presentar los datos en este Notebook. Los cinco estilos son darkgrid, whitegrid, dark, white, and ticks. Mostramos con este código todos los estilos. Para escoger uno solo para el resto del notbook agrega al código "sns.set_style("nombre del estilo")"
"""

def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']

f = plt.figure()
for i in range(len(styles)):
  with sns.axes_style(styles[i]):   # Con with puedes aplicar un estilo solo una vez
    ax = f.add_subplot(2,3,i+1)
    ax.set_title(styles[i])
    sinplot()

sns.set_context("paper")

"""## Preparando el DataSet

Utilizaremos el "Iris plant dataSet" en [`sklearn.datasets`](https://scikit-learn.org/stable/datasets/index.html#toy-datasets). ¿Cuántas instancias (datos) tenemos? ¿Cuántos predictores se tienen? ¿Qué se desea predecir?
"""

from sklearn.datasets import load_iris

iris = load_iris()

print(iris.keys())
print(iris["DESCR"])

"""Convierte los datos a un DataFrame en panda, y muestra ~.head()"""

ir = pd.DataFrame(iris.data, columns=iris.feature_names)

ir.head()

"""¿Cuál es la correlación entre las *clases* de flores?

*Ayuda: Debe de conseguir el mismo resultado que el que se halla en la descripción de los datos.*
"""

cols = list(ir)
print(cols)

coefs = np.corrcoef(ir.values.T)
heatMap = sns.heatmap(coefs, annot = True, yticklabels=cols, xticklabels=cols)

"""### Preguntas

Para cada una de las especies de planta, trata de predecir el ancho del sépalo usando las otras tres variables como predictores. Responde a los siguientes:

#### 1

Ajusta una regresión lineal simple entre cada predictor al ancho de sépalo. ¿En cuáles de los modelos hay una asociación significativa entre predictor y respuesta? Haz gráficas para respaldar tu respuesta.
"""

import statsmodels.formula.api as smf

y=ir["sepal length (cm)"].reshape(-1,1)
x=ir["sepal width (cm)"].reshape(-1,1)


est = smf.ols(formula="x~y", data = ir).fit()
print(est.summary().tables[1])

y=ir["petal width (cm)"].reshape(-1,1)
x=ir["sepal width (cm)"].reshape(-1,1)


est = smf.ols(formula="x~y", data = ir).fit()
print(est.summary().tables[1])

y=ir["petal length (cm)"].reshape(-1,1)
x=ir["sepal width (cm)"].reshape(-1,1)


est = smf.ols(formula="x~y", data = ir).fit()
print(est.summary().tables[1])

"""#### 2
¿Al menos uno de los predictores es útil para predecir el ancho del sépalo? Haga una prueba de hipótesis para esto.
"""

#Predecir
y=ir["sepal length (cm)"].reshape(-1,1)
x=ir["sepal width (cm)"].reshape(-1,1)

lr=LinearRegression()
lr.fit(x,y)

y_pred=lr.predict(x)
     
plt.scatter(x,y, color="black")
plt.plot(x,y_pred, color="blue", linewidth=1)

"""#### 3
Considera solo una especie de planta y el modelo generado para predecir el ancho de sépalo. ¿Este funciona bien para las otras especies? Prueba usar los datos de Iris-Setosa como entrenamiento para algún modelo de regresión y úsalo para predecir el ancho de sépalo de las otras dos especies. ¿Hay una diferencia significativa entre las predicciones hechas para cada especie?
"""

##select de las flores Setosa
setosa = ir.iloc[ :49 , : ]
setosa.head()

y=setosa["petal width (cm)"].values.reshape(-1,1)
x=setosa["sepal width (cm)"].values.reshape(-1,1)


#entrenamiento del modelo con Setosa
est = smf.ols(formula="x~y", data = setosa).fit()
print(est.summary().tables[1])

rss = np.sum((ir["sepal width (cm)"] - est.params.Intercept + (est.params.y*ir["petal width (cm)"]))**2)
rss

#calculo del Error Estandar Residual
RSE = np.sqrt(rss/(48))
RSE

##select de las flores Versicolor
versicolor = ir.iloc[ 50:99 , : ]
versicolor.head()

y=versicolor["petal width (cm)"].values.reshape(-1,1)
x=versicolor["sepal width (cm)"].values.reshape(-1,1)

#entrenamiento del modelo con Versicolor
est = smf.ols(formula="x~y", data = versicolor).fit()
print(est.summary().tables[1])

rss = np.sum((ir["sepal width (cm)"] - est.params.Intercept + (est.params.y*ir["petal width (cm)"]))**2)
rss

#calculo del Error Estandar Residual
RSE = np.sqrt(rss/(48))
RSE

##select de las flores Virginica
virginica = ir.iloc[ 100: , : ]
virginica.head()

y=virginica["petal width (cm)"].values.reshape(-1,1)
x=virginica["sepal width (cm)"].values.reshape(-1,1)

#entrenamiento del modelo con Virginica
est = smf.ols(formula="x~y", data = virginica).fit()
print(est.summary().tables[1])

rss = np.sum((ir["sepal width (cm)"] - est.params.Intercept + (est.params.y*ir["petal width (cm)"]))**2)
rss

#calculo del Error Estandar Residual
RSE = np.sqrt(rss/(48))
RSE

"""Debido a los valores obtenidos en el Error Estandar Residual (RSE), hay diferencias significativas por lo cual las predicciones varian demasiado.

#### 4
¿Tiene alguna limitante el modelo lineal en este tipo de datos? ¿Qué otro tipo de algoritmo cree que mejoraría su poder de predicción?

No porque solo se definen las 2 variables que se desea graficar. 

Ninguno porque la regresión linear es la que tiene un mejor intervalo de confianza.
"""