# -*- coding: utf-8 -*-
"""Tarea4 Juan Jose .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fx5vQlnldzGrWMayf_cDa1TVtB9MLoSs

# Ejercicios aplicados: Selección de predictores (mejores subconjuntos y Lasso)

(Ejercicio 8 del capítulo 6 del libro:)



1.   Genera un predictor $X$ con $n=100$ observaciones aleatorias entre $[0,1]$. Genera también un vector de ruido $\epsilon$ con $n=100$ valores aleatorios
"""

import itertools
import time
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from tqdm import tnrange, tqdm_notebook

x=np.random.normal(0.5,0.19,100)
x

"""2. Evalúa $Y=\beta_0+\beta_1X+\beta_2X^2+\beta_3X^3+\epsilon$ donde los $\beta$ son de tu elección (para ver un ejemplo de cómo generar datos de esta manera, ver: https://www.analyticsvidhya.com/blog/2017/06/a-comprehensive-guide-for-linear-ridge-and-lasso-regression/)"""

y= 0.1+0.2*x[1]+0.3*x[2]*x[2]+0.4*x[3]*x[3]*x[3]+epsilon
y

"""3.   Haz una selección de mejores subconjuntos (best subsets selection) y muestra cuál es el mejor modelo de acuerdo a $C_p$, BIC y $R^2$ ajustado"""

#Concat values
df1 = pd.DataFrame(data=x,columns=['x'])
df2 = pd.DataFrame(data=y,columns=['y'])
df=pd.concat([df1, df2], axis=1)

def linear(X,Y):
    mk = linear_model.LinearRegression(fit_intercept = True)
    mk.fit(X,Y)
    RSS = mean_squared_error(Y,mk.predict(X)) * len(Y)
    R_squared = mk.score(X,Y)
    return RSS, R_squared
  
Y = df.x
X = df.drop(columns = 'x', axis = 1)
k = 11
RSS, R_squared, feature = [],[], []
num = []

for k in tnrange(1,len(X.columns) + 1, desc = 'Loop...'):

    for combo in itertools.combinations(X.columns,k):
        tmp_result = fit_linear_reg(X[list(combo)],Y)   
        RSS.append(tmp_result[0])                  
        R_squared.append(tmp_result[1])
        feature.append(combo)
        num.append(len(combo))   

#Create Dataframe
df3 = pd.DataFrame({'num': num,'RSS': RSS, 'R_squared':R_squared,'features':feature})

#Find best subset for each number of features
df3_min = df3[df3.groupby('num')['RSS'].transform(min) == df3['RSS']]
df3_max = df3[df3.groupby('num')['R_squared'].transform(max) == df3['R_squared']]

#Add columns RSS & R squared values to df
df3['min_RSS'] = df3.groupby('num')['RSS'].transform(min)
df3['max_R_squared'] = df3.groupby('num')['R_squared'].transform(max)

#Plotting
fig = plt.figure(figsize = (16,6))
ax = fig.add_subplot(1, 2, 1)

ax.scatter(df3.num,df3.RSS, alpha = .2, color = 'darkblue' )
ax.set_xlabel('# Features')
ax.set_ylabel('RSS')
ax.set_title('RSS - Best subset selection')
ax.plot(df3.num,df3.min_RSS,color = 'r', label = 'Best subset')
ax.legend()

ax = fig.add_subplot(1, 2, 2)
ax.scatter(df3.num,df3.R_squared, alpha = .2, color = 'darkblue' )
ax.plot(df3.num,df3.max_R_squared,color = 'r', label = 'Best subset')
ax.set_xlabel('# Features')
ax.set_ylabel('R squared')
ax.set_title('R_squared - Best subset selection')
ax.legend()

plt.show()

"""4.   Repite lo anterior ahora usando *forward stepwise selection* y también con *backward stepwise selection*."""

Y = df.y
X = df.drop(columns = 'y', axis = 1)
k = 11

remaining_features = list(X.columns.values)
features = []
RSS_list, R_squared_list = [np.inf], [np.inf]
features_list = dict()

for i in range(1,k+1):
    best_RSS = np.inf
    
    for combo in itertools.combinations(remaining_features,1):
            RSS = fit_linear_reg(X[list(combo) + features],Y)  
            if RSS[0] < best_RSS:
                best_RSS = RSS[0]
                best_R_squared = RSS[1] 
                best_feature = combo[0]

    features.append(best_feature)
    remaining_features.remove(best_feature)
    
    RSS_list.append(best_RSS)
    R_squared_list.append(best_R_squared)
    features_list[i] = features.copy()

"""5.   Ahora haz regressión Lasso y usa validación cruzada para encontrar el mejor $\lambda$ para los datos.
6.   Discute cómo se comparan los cuatro métodos usados)

# Nuevos conceptos

Lee las secciones 6.3 y 6.4 de *Introduction* para contestar los siguientes:

### Sección 6.3
1.   Explica a grandes rasgos en qué consiste la reducción de orden por PCR
>Es una técnica basada en PCA. La idea básica es calcular componentes principales y utilizar algunos de estos como predictores en una regresión lineal utilizando los cuadrantes mínimos.

2.   PCR reduce la cantidad de predictores de r a M. A pesar de esto, ¿por qué no se considera a PCR como un método de selección de predictores?
> Porque cada uno de los componentes principales calculados es una combinación lineal de variables originales. No utilizar las variables originales complica la explicación de lo que se hizo.

3.   PCR es un método no supervisado mientras que PLS es supervisado. Explica por qué existe esta diferencia.
>La variable dependiente no es utilizada para identificar la dirección de cada componente principal por lo cual no es lo optimo para hacer predicciones.

### Sección 6.4
1.   ¿Qué situaciones son de alta dimensión? ¿Qué problemas surgen en estas situaciones?
>Data sets que tienen más features que observaciones (p>n) y cuando p es ligeramente mas pequeño que n.

>Cuadros minimos no se pueden hacer por las variables obtenidas. Cuando sse tienen dos observaciones la regresión será exacta.

2.   Entre todos los métodos para generar modelos, indica cuáles son apropiados en altas dimensiones y cuáles no, y por qué.
>Lasso, Ridge, componentes principales regresión, forward y backward selection son buenos por las dimensiones que utilizan.

### De *Elements*
Lee la sección 3.4.3 de *Elements* para explicar la penalización *elastic-net* (la describen hasta el final de la sección)
>seleciona variables como Lasso & reduce juntos los coeficientes correlacionados con los predictores como ridge. Utiliza la penalización de Lasso y Ridge
"""