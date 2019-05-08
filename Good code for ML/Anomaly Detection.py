# -*- coding: utf-8 -*-
"""Anomaly detection - master.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ONBrftzt2v9tosIQVpq7QlPbRaV6UP1

Original data from Kaggle: https://www.kaggle.com/c/expedia-personalized-sort/data

Article that this lab is based on: https://towardsdatascience.com/time-series-of-price-anomaly-detection-13586cd5ff46

# Import packages
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""# Import data"""

# Original data importation and single hotel extraction
# expedia = pd.read_csv('train.csv')
# df = expedia.loc[expedia['prop_id'] == 104517]
# df = df.loc[df['srch_room_count'] == 1]
# df = df.loc[df['visitor_location_country_id'] == 219]
# expedia_df = df[['date_time', 'price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
# expedia_df = expedia_df.loc[df['price_usd'] < 5584]
# expedia_df.to_csv('expedia_train.csv', index = False)

# expedia = pd.read_csv('test.csv')
# df = expedia.loc[expedia['prop_id'] == 104517]
# df = df.loc[df['srch_room_count'] == 1]
# df = df.loc[df['visitor_location_country_id'] == 219]
# expedia_df = df[['date_time', 'price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
# expedia_df = expedia_df.loc[df['price_usd'] < 5584]
# expedia_df.to_csv('expedia_test.csv', index = False)

# Read in train and test files (already pre split in source)
expedia_train = pd.read_csv('expedia_train.csv')
# expedia_test = pd.read_csv('expedia_test.csv')

# Simplified training df
expedia_train.head()

# 3048 observations, no unreasonable values
expedia_train.describe()

# No NAs
expedia_train.isna().sum()

# Changing the type to datetime for plotting
expedia_train['date_time'] = pd.to_datetime(expedia_train['date_time'])
# expedia_test['date_time'] = pd.to_datetime(expedia_test['date_time'])

# Entire training set
sns.lineplot(x='date_time', y = 'price_usd', data = expedia_train)

# Last 100 prices
sns.lineplot(x='date_time', y = 'price_usd', data = expedia_train.tail(100))

"""# Finding outliers using K-means"""

from sklearn.cluster import KMeans

# Examining added benefit of additional clusters for training score
data = expedia_train[['price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
n_cluster = range(1, 20)
kmeans = [KMeans(n_clusters=i).fit(data) for i in n_cluster]
scores = [kmeans[i].score(data) for i in range(len(kmeans))]

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(n_cluster, scores)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show();

# Create 10 clusters
X = expedia_train[['price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
X = X.reset_index(drop=True)
km = KMeans(n_clusters=10)
km.fit(X)
km.predict(X)
labels = km.labels_

# Finding observations that are farthest from their respective centroid
def getDistanceByPoint(data, model):
    distance = pd.Series()
    for i in range(0,len(data)):
        Xa = np.array(data.loc[i])
        Xb = model.cluster_centers_[model.labels_[i]-1]
        distance.set_value(i, np.linalg.norm(Xa-Xb))
    return distance

outliers_fraction = 0.01
# Get the distance between each point and its nearest centroid. The biggest distances are considered as anomaly
distance = getDistanceByPoint(data, kmeans[9])
number_of_outliers = int(outliers_fraction*len(distance))
threshold = distance.nlargest(number_of_outliers).min()
# anomaly1 contain the anomaly result of the above method Cluster (0:normal, 1:anomaly) 
expedia_train['anomaly1'] = (distance >= threshold).astype(int)

# visualisation of anomaly with cluster view
fig, ax = plt.subplots(figsize=(10,6))
colors = {0:'blue', 1:'red'}
ax.scatter(expedia_train['srch_booking_window'], expedia_train['price_usd'], c=expedia_train['anomaly1'].apply(lambda x: colors[x]))
plt.xlabel('srch_booking_window')
plt.ylabel('price_usd')
plt.show();

# Now price vs datetime
expedia_train = expedia_train.sort_values('date_time')
expedia_train['date_time_int'] = expedia_train.date_time.astype(np.int64)
fig, ax = plt.subplots(figsize=(10,6))
a = expedia_train.loc[expedia_train['anomaly1'] == 1, ['date_time_int', 'price_usd']] #anomaly

ax.plot(expedia_train['date_time_int'], expedia_train['price_usd'], color='blue', label='Normal', alpha = 0.6)
ax.scatter(a['date_time_int'],a['price_usd'], color='red', label='Anomaly')
plt.xlabel('Date Time Integer')
plt.ylabel('price in USD')
plt.legend()
plt.show();

"""# Isolation forests"""

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

data = expedia_train[['price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
scaler = StandardScaler()
np_scaled = scaler.fit_transform(data)
data = pd.DataFrame(np_scaled)
# train isolation forest
model =  IsolationForest(contamination=outliers_fraction)
model.fit(data) 
expedia_train['anomaly2'] = pd.Series(model.predict(data))

# visualization
fig, ax = plt.subplots(figsize=(10,6))

a = expedia_train.loc[expedia_train['anomaly2'] == -1, ['date_time_int', 'price_usd']] #anomaly

ax.plot(expedia_train['date_time_int'], expedia_train['price_usd'], color='blue', label = 'Normal', alpha = 0.6)
ax.scatter(a['date_time_int'],a['price_usd'], color='red', label = 'Anomaly')
plt.legend()
plt.show();

"""# One Class SVM"""

from sklearn.svm import OneClassSVM

data = expedia_train[['price_usd', 'srch_booking_window', 'srch_saturday_night_bool']]
scaler = StandardScaler()
np_scaled = scaler.fit_transform(data)
data = pd.DataFrame(np_scaled)
# train oneclassSVM 
model = OneClassSVM(nu=outliers_fraction, kernel="rbf", gamma=0.01)
model.fit(data)
expedia_train['anomaly3'] = pd.Series(model.predict(data))

fig, ax = plt.subplots(figsize=(10,6))
a = expedia_train.loc[expedia_train['anomaly3'] == -1, ['date_time_int', 'price_usd']] #anomaly

ax.plot(expedia_train['date_time_int'], expedia_train['price_usd'], color='blue', alpha = 0.6)
ax.scatter(a['date_time_int'],a['price_usd'], color='red')
plt.show();

"""# Gaussian distribution"""

from sklearn.covariance import EllipticEnvelope

df_class0 = expedia_train.loc[expedia_train['srch_saturday_night_bool'] == 0, 'price_usd']
df_class1 = expedia_train.loc[expedia_train['srch_saturday_night_bool'] == 1, 'price_usd']

envelope =  EllipticEnvelope(contamination = outliers_fraction) 
X_train = df_class0.values.reshape(-1,1)
envelope.fit(X_train)
df_class0 = pd.DataFrame(df_class0)
df_class0['deviation'] = envelope.decision_function(X_train)
df_class0['anomaly'] = envelope.predict(X_train)

envelope =  EllipticEnvelope(contamination = outliers_fraction) 
X_train = df_class1.values.reshape(-1,1)
envelope.fit(X_train)
df_class1 = pd.DataFrame(df_class1)
df_class1['deviation'] = envelope.decision_function(X_train)
df_class1['anomaly'] = envelope.predict(X_train)

df_class = pd.concat([df_class0, df_class1])
expedia_train['anomaly5'] = df_class['anomaly']
fig, ax = plt.subplots(figsize=(10, 6))
a = expedia_train.loc[expedia_train['anomaly5'] == -1, ('date_time_int', 'price_usd')] #anomaly
ax.plot(expedia_train['date_time_int'], expedia_train['price_usd'], color='blue', alpha = 0.6)
ax.scatter(a['date_time_int'],a['price_usd'], color='red')
plt.show();