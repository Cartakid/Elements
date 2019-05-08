# -*- coding: utf-8 -*-
"""Polynomial regression - master.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sCt9I8lzJc3OIL-tJLm8w3PnIeL8Ra2z

# Import packages
"""

!pip install statsmodels

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.stats.anova import anova_lm
import sklearn.metrics

"""# Import data"""

# Import data from URL and add column names
auto_df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data', header = None
                     , na_values = '?')

auto_df.columns = [
 'symboling'
 ,'normalized-losses'
 ,'make'
 ,'fuel-type'
 ,'aspiration'
 ,'num-of-doors'
 ,'body-style'
 ,'drive-wheels'
 ,'engine-location'
 ,'wheel-base'
 ,'length'
 ,'width'
 ,'height'
 ,'curb-weight'
 ,'engine-type'
 ,'num-of-cylinders'
 ,'engine-size'
 ,'fuel-system'
 ,'bore'
 ,'stroke'
 ,'compression-ratio'
 ,'horsepower'
 ,'peak-rpm'
 ,'city-mpg'
 ,'highway-mpg'
 , 'price'
]

# Top 5 rows to get a sense of what the data looks like
auto_df.head()

"""# Data imputation"""

# Impute values for columns with NAs
auto_df['normalized-losses'].fillna(auto_df['normalized-losses'].median(), inplace=True)
auto_df['num-of-doors'].fillna(auto_df['num-of-doors'].mode(), inplace=True)
auto_df['bore'].fillna(auto_df['bore'].median(), inplace=True)
auto_df['stroke'].fillna(auto_df['stroke'].median(), inplace=True)
auto_df['horsepower'].fillna(auto_df['horsepower'].median(), inplace=True)
auto_df['peak-rpm'].fillna(auto_df['peak-rpm'].median(), inplace=True)
auto_df['price'].fillna(auto_df['price'].median(), inplace=True)

"""# Data exploration"""

# Response variable does have significant skew
sns.distplot(auto_df['price'])

"""# Modeling preparation"""

# Isolate response variable
y = pd.DataFrame(auto_df['price'])

y.head()

# Drop response variable from feature dataframe
X = auto_df.drop('price', axis=1)

X.shape

X.head()

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

"""# Linear and polynomial modeling"""

# Plot response variable vs feature of interest
sns.scatterplot(x='horsepower', y='price', data=auto_df)

# Train linear model
X_train = sm.add_constant(X_train)
simple_model = sm.OLS(y_train,X_train[['horsepower', 'const']])

simple_result = simple_model.fit()

# Predict on test set and plot results
X_test = sm.add_constant(X_test)
y_pred_simple = simple_result.predict(X_test[['horsepower', 'const']])
sns.scatterplot(x = X_test['horsepower'], y = y_test.values.ravel())
sns.lineplot(x = X_test['horsepower'] , y = y_pred_simple)

# Print evaluation metrics table
print(simple_result.summary())

# Create polynomial regression features of nth degree
poly_reg = PolynomialFeatures(degree = 5)
X_poly_train = poly_reg.fit_transform(pd.DataFrame(X_train['horsepower']))
X_poly_test = poly_reg.fit_transform(pd.DataFrame(X_test['horsepower']))
poly_result = poly_reg.fit(X_poly_train, y_train)

# Fit linear model now polynomial features
poly_model = LinearRegression()
poly_result = poly_model.fit(X_poly_train, y_train)
y_poly_pred = poly_model.predict(X_poly_test)

# Plot to compare models
sns.scatterplot(x = X_test['horsepower'], y = y_test.values.ravel())
sns.lineplot(x = X_test['horsepower'] , y = y_pred_simple)
sns.lineplot(x = X_test['horsepower'] , y = y_poly_pred.ravel())

# Retrain to be able to print summary table
poly_model = sm.OLS(y_train,X_poly_train)
poly_result = poly_model.fit()

#y_poly_pred = poly_model.predict(X_poly_test)

# Print model evaluation metrics
print(poly_result.summary())

"""# ANOVA testing"""

# Compare the two models using an ANOVA test
anovaResults = anova_lm(simple_result, poly_result)
print(anovaResults)

