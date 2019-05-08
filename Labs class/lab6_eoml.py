# -*- coding: utf-8 -*-
"""Laboratorio 6 Juan Jose - EoML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jdYOmCT1a3D7IsJ5t3Ky-WlkJG7u5Qek

# Laboatorio 6

En este laboratorio usaremos bootstrap para hacer estimaciones de la media y desviación estándar de algún estadístico de un grupo de datos.
"""

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import statsmodels
import statsmodels.formula.api as smf

from sklearn.model_selection import KFold

print("Todos los paquetes han sido importados:")

"""## Un ejemplo de bootstrap

Escribimos aquí lo que vimos en la presentación en clase: usamos la función resample de sklearn para realizar bootstrap sobre un grupo de datos
"""

from sklearn.utils import resample

mean = [0,0]
cov = [[1.,0.25],[0.25,1.25]]

# Generamos observaciones (X,Y) a partir de una distribución aleatoria
np.random.seed(1)
X, Y = np.random.multivariate_normal(mean, cov, 100).T
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)

alphas_hat = []

for _ in range(1000):
  X1, Y1 = resample(X, Y, replace=True, n_samples=100)
  [s_X, s_XY, _, s_Y] = np.cov(X1.T, Y1.T).reshape(-1, 1)
  alphas_hat.append(float((s_Y-s_XY)/(s_X+s_Y-2*s_XY)))

alpha_mean = np.mean(alphas_hat)
alpha_err = np.std(alphas_hat, ddof=1)
print(alpha_mean)

"""### Ejercicio 1

Basándote en el código anterior, haz una función bootstrap que tome como argumento un dataset y que regrese la media y desviación estándar del R^2 de una regresión lineal aplicada entre X y Y. Es decir, haz una función que usa bootstrap para encontrar un intervalo de confianza para el estadístico R^2 de una regresión lineal.
"""

#Upload file
from google.colab import files
uploaded = files.upload()
import pandas as pd
import io
auto= pd.read_csv(io.BytesIO(uploaded['Auto.csv']))

from sklearn.linear_model import LinearRegression

mean = [0,0]
cov = [[1.,0.25],[0.25,1.25]]

# Generamos observaciones (X,Y) a partir de una distribución aleatoria
np.random.seed(1)
X, Y = np.random.multivariate_normal(mean, cov, 100).T
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)

alphas_hat = []

for _ in range(1000):
  X1, Y1 = resample(X, Y, replace=True, n_samples=100)
  #[s_X, s_XY, _, s_Y] = np.cov(X1.T, Y1.T).reshape(-1, 1)
  #alphas_hat.append(float((s_Y-s_XY)/(s_X+s_Y-2*s_XY)))

alpha_mean = np.mean(alphas_hat)
alpha_err = np.std(alphas_hat, ddof=1)
print(alpha_mean)

"""## Ejercicio de aplicación

Utiliza los datos de cáncer de mama (los del laboratorio 3) y el procedimiento de bootstrap para hacer estimaciones de la media y desviación estándar de los coeficientes que arroja una regresión logística múltiple y compara estas estimaciones con las que da la regresión sobre la muestra original
"""

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
bc = pd.DataFrame(data.data, columns=data.feature_names) # 30 predictores
bc["Clase"] = pd.DataFrame(data.target, columns=['Clase']) # clase (benigno o maligno)