# -*- coding: utf-8 -*-
"""Laboratorio 3 Juan Jose EoML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10HgkMKfAzfuJ6aqrw2kqzyGkRlmAuneQ

# Laboatorio 3

En este laboratorio aplicaremos regresión logística simple y múltiple a un dataset de pasajeros del titanic para explorar las probabilidades de supervivencia respecto a predictores como edad, sexo y precio de boleto.
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

"""## Ejemplo de regresión logística: Cáncer de mama

Usando un dataset tomado de sklearn de cáncer de mama, mostraremos modelos de regresión logística para algunos de los predictores
"""

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
bc = pd.DataFrame(data.data, columns=data.feature_names) # 30 predictores
bc["Clase"] = pd.DataFrame(data.target, columns=['Clase']) # clase (benigno o maligno)

bc.head()

bc["Clase"].head()

"""Verifiquemos que el target es binario"""

sns.countplot(x='Clase',data=bc, palette='hls')

"""Haremos una regresión logística entre el radio del tumor y la clase"""

est = smf.Logit(bc['Clase'], bc["mean radius"]).fit()
est.summary2()

"""Los números de interés que arroja .summary2() son el coeficiente y el valor z. Un valor z mayor a 1.96 indica que existe una relación significativa entre el predictor y el target. El número e^coeficiente es una medida de cuánto aumenta el valor del target para aumentos en 1 del predictor. En este caso, vemos que la relación entre el radio medio y la clase de tumor es no significativa.

Haremos una regresión múltiple con los primeros 5 predictores de bc
"""

est = smf.Logit(bc['Clase'], bc[bc.columns[0:5]]).fit()
est.summary2()

"""### Ejercicios



1.  ¿Cómo interpretas los resultados de la última tabla generada?
2.   Haz una regresión lineal equivalente para las regresiones logísticas que hicimos y compara los resultados. ¿Qué concluye la regresión lineal sobre la hipótesis nula entre los predictores y la clase? ¿Es diferente esta conclusión a la que vemos con la regresión logística?

1. Indica que existe una relación significativa entre Clase y Mean Radius mientras que con las otras columnas no hay relación.  El valor de Mean Radius aumenta 8 cuando la clase aumenta 1, para las demás variables no hay relación de coeficiente.
"""

bc=bc.rename(index=str, columns={"mean radius": "mr","mean texture": "mt","mean perimeter": "mp","mean area": "ma","mean smoothness": "ms"})
lr = smf.ols('Clase ~ mr+mt+mp+ma+ms', data=bc).fit()
lr.summary()

"""No hay relacion entre el predictor y los target porque no es significativa. Si cambia la conclusión porque en la primera regresión es más fácil ver la relación entre el predictor y el target.

## Datos de Titanic

Ahora usa los datos de supervivencia de Titanic encontrados en https://www.kaggle.com/c/titanic.

### Ejercicios



1.   Explora los datos de Titanic: identifica si hay datos perdidos y haz histogramas de los predictores (por lo menos 4) para darte una idea de los datos
2.   Haz una regresión logística múltiple de todos los predictores y la supervivencia de los pasajeros e interpreta los resultados. ¿Cuál de los predictores parece ser el más importante para determinar quién sobrevive o no, según una regresión logística múltiple?
"""

from google.colab import files
uploaded = files.upload()
import io
titanic= pd.read_csv(io.BytesIO(uploaded['train.csv']))

ship=pd.DataFrame(data=titanic)
ship.head()

sns.countplot(x='Sex',data=ship, palette='hls')

sns.countplot(x='Pclass',data=ship, palette='hls')

sns.countplot(x='Embarked',data=ship, palette='hls')

sns.countplot(x='Survived',data=ship, palette='hls')

ship.fillna({'Pclass':ship["Pclass"].mean(), 'Age':ship["Age"].mean(), 'SibSp':ship["SibSp"].mean(), 'Parch':ship["Parch"].mean(), 'Fare':ship["Fare"].mean()}, inplace=True)
reg=smf.Logit(ship["Survived"],ship[["Pclass", "Age", "SibSp", "Parch", "Fare"]]).fit()
reg.summary2()

"""Ningún target indica relación de supervivencia porque uno sobrevive por otros factores que no están analizados."""