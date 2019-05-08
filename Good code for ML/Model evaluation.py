# -*- coding: utf-8 -*-
"""Class 11: Model evaluation - master.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uS88mkRWqy5w4wMceRPyJZgSs3XMo_Ak

# Import packages
"""

! pip install mlxtend

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import log_loss
from sklearn.metrics import silhouette_samples

"""# Import data"""

# Import data from URL and add column names
wine_df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data', header = None)
wine_df.columns = ['Label', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 
                   'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 
                   'OD280/OD315 of diluted wines', 'Proline']

"""# Initial data exploration"""

# Show value counts of response variable
wine_df['Label'].value_counts()

# Distribution plot of a feature
sns.distplot(wine_df['Alcohol'])

"""# Transform and split data"""

# Separate labels, so we don't scale the categorical values
wine_features = wine_df.iloc[:, 1:]
wine_labels = wine_df.iloc[:,0]

# Normalize data so each variable has appropriate influence
sc = StandardScaler()
wine_features_std = sc.fit_transform(wine_features)

# Convert numpy array to pandas dataframe and add columns back
wine_features_std = pd.DataFrame(wine_features_std)
wine_features_std.columns = wine_features.columns

X_train, X_test, y_train, y_test = train_test_split(wine_features_std, wine_labels, test_size=0.25, random_state=42)

X_train.head()

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

"""# Build a model"""

# Define and fit standardized data
lda = LDA()
ld = lda.fit_transform(X_train, y_train)
lda_df = pd.DataFrame(data = ld, 
        columns = ['LDA1', 'LDA2'])
lda_df['Cluster'] = y_train

# Print results of classification of training data
print('Accuracy of LDA classifier on training set: {:.2f}'
     .format(lda.score(X_train, y_train)))
# print('Accuracy of LDA classifier on test set: {:.2f}'
#      .format(lda.score(X_test, y_test)))

# Print top n observations of LDA df
lda_df.head()

# Function that will score your predictions on the test set in terms of accuracy
lda.score(X_test, y_test)

# Returns the predicted values for your test set
lda_pred = lda.predict(X_test)

print(pd.Series(lda_pred).value_counts())
y_test.value_counts()

"""# Confusion matrix with three levels"""

cm = confusion_matrix(y_true = y_test, y_pred = lda_pred)
print(cm)

# Plot confusion matrix
# http://rasbt.github.io/mlxtend/user_guide/evaluate/confusion_matrix/
fig, ax = plot_confusion_matrix(conf_mat=cm)
plt.show()

"""# Build out model 2"""

# Transform response variable into 2 levels for binomial prediction
def response(series):
    if series >= 2:
        return 1
    else:
        return 0

# Apply the response function to all training and testing samples
y_train2 = y_train.apply(response)
y_test2 = y_test.apply(response)
print(y_train2.value_counts())
print(y_test2.value_counts())

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
lr = logreg.fit(X_train, y_train2)

# Coefficients and intercept of logistic regression equation
print(lr.coef_)
print(lr.intercept_)

# Accuracy of predictions on test set
lr.score(X_test, y_test2)

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
lr = logreg.fit(X_train.iloc[:, 2:4], y_train2)

# Coefficients and intercept of logistic regression equation
print(lr.coef_)
print(lr.intercept_)

# Accuracy of predictions on test set
lr.score(X_test.iloc[:, 2:4], y_test2)

# Prediction probabilities of test set
lr_pred = lr.predict(X_test.iloc[:, 2:4])

"""# Confusion matrix 2"""

# Confusion matrix of predictions
cm2 = confusion_matrix(y_true = y_test2, y_pred = lr_pred)
print(cm2)

# Plotted confusion matrix
fig, ax = plot_confusion_matrix(conf_mat=cm2)
plt.show()

"""# ROC curve"""

# Predicted probability of belonging to response class 1
pred_prob = lr.predict_proba(X_test.iloc[:, 2:4])[:,1]
pred_prob

# Get array of false positive rate, true positive rate, and "decreasing thresholds on the decision function used to compute fpr and tpr"
# Decreasing thresholds on the decision function used to compute fpr and tpr
fpr, tpr, thresholds = metrics.roc_curve(y_test2, pred_prob)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='LR')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')
plt.legend(loc='best')
plt.show()

"""# AUC"""

# Area under the curve
metrics.auc(fpr, tpr)

"""# Log loss"""

# Predicted probabilities on training set
pred_prob_train = lr.predict_proba(X_train.iloc[:, 2:4])[:,1]

# Log loss on training set
log_loss(y_true = y_train2, y_pred = pred_prob_train)

# Log loss on testing set
log_loss(y_true = y_test2, y_pred = pred_prob)

"""# Silhouette coefficient"""

# Silhouette coefficient for each observation in test set
silhouette_dist = silhouette_samples(X_test.iloc[:, 2:4], y_test2, metric='euclidean')

# Histogram of silhouette coefficient distribution
sns.distplot(silhouette_dist)
