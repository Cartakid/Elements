# -*- coding: utf-8 -*-
"""Neural Networks pt1 - keras - master.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OzoOjijAsbdj5NFCzkbsAlHk5Vez9LJl

# Into to TensorFlow 2.0 and keras

Keras is the "high-level" API for Tensorflow.
"""

# !pip install tensorflow=='2.0.0-alpha0'

import tensorflow as tf

tf.__version__

from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard 

import numpy as np
from time import time
import matplotlib.pyplot as plt

"""### load dataset

Classic MNIST dataset which includes hand written numbers.
"""

mnist = keras.datasets.fashion_mnist

(X_train, y_train) , (X_test, y_test) = mnist.load_data()

label_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

X_train.shape, X_test.shape

y_train.shape, y_test.shape

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(X_train[i], cmap=plt.cm.binary)
    plt.xlabel(label_names[y_train[i]])
plt.show()

"""## Model building (Your first Neural Network!)

![neural_net](https://pluralsight.imgix.net/course-images/keras-deep-learning-v1.png)
"""

from tensorflow.keras.layers import Dense, Flatten, Activation

"""### Start with the type of model

`keras.Sequential()` will give us the common forward propagating network.
"""

first_model = keras.Sequential()

"""### Now add your layers

`Dense` refers to the fully connected layer.

parameters:
 - `units`: Positive integer, dimensionality of the output space.
 - `activation`: Activation function to use (see activations). If you don't specify anything, no activation is applied (ie. "linear" activation: a(x) = x).
 - `use_bias`: Boolean, whether the layer uses a bias vector. Its default value is `True`.

`Activation` will apply the activation function to your outputs. You can also just use the `Dense(activation='')` parameter.

`Flatten` Will flatten out a matrix input into a vector

adding the **input layer**
"""

# Add the layers by calling model.add()

first_model.add(Flatten(input_shape=(28, 28)))

"""adding the **hidden layer**"""

first_model.add(Dense(64, activation='sigmoid'))

"""and our final **output layer**"""

first_model.add(Dense(10, ))

"""print out the layers"""

first_model.get_config()

"""### Compiling your model

`model.Compile()` will compile your model with the given layers and parameters for training.

parameters:

- `optimizer`: String (name of optimizer) or optimizer instance. See optimizers.
- `loss`: String (name of objective function) or objective function. See losses. If the model has multiple outputs, you can use a different loss on each output by passing a dictionary or a list of losses. The loss value that will be minimized by the model will then be the sum of all individual losses.
- `metrics`: List of metrics to be evaluated by the model during training and testing. Typically you will use `metrics=['accuracy']`. To specify different metrics for different outputs of a multi-output model, you could also pass a dictionary, such as `metrics={'output_a': 'accuracy'}`.
"""

first_model.compile(optimizer = 'sgd',
                    loss = 'sparse_categorical_crossentropy',
                    metrics = ['accuracy'])

"""### Now on to training!

`model.fit()` will compile your model with the given layers and parameters for training.

parameters:
Arguments

- `x`: Numpy array of training data 
- `y`: Numpy array of target (label) data 
- `batch_size`: Mini batch size
- `epochs`: Integer. Number of epochs to train the model. An epoch is an iteration over the entire x and y data provided.
- `verbose`: Integer. 0, 1, or 2. Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch.
- `callbacks`: List of keras.callbacks.Callback instances. List of callbacks to apply during training and validation.
- `validation_split`: Float between 0 and 1. Fraction of the training data to be used as validation data. 
- `validation_data`: tuple (x_val, y_val) or tuple  (x_val, y_val, val_sample_weights) on which to evaluate the loss and any model metrics at the end of each epoch. The model will not be trained on this data. 
- `shuffle`: Boolean (whether to shuffle the training data before each epoch).
- `class_weight`: Optional dictionary mapping class indices (integers) to a weight (float) value, used for weighting the loss function (during training only). This can be useful to tell the model to "pay more attention" to samples from an under-represented class.
- `validation_freq`: Only relevant if validation data is provided. Integer or list/tuple/set. If an integer, specifies how many training epochs to run before a new validation run is performed, e.g. validation_freq=2 runs validation every 2 epochs. If a list, tuple, or set, specifies the epochs on which to run validation, e.g. validation_freq=[1, 2, 10] runs validation at the end of the 1st, 2nd, and 10th epochs.
"""

model_history = first_model.fit(x = X_train,
                                y = y_train,
                                batch_size = 128,
                                epochs = 5,
                                validation_split = 0.2,
                                shuffle=True)

model_history.history

print(model_history.history.keys())
# summarize history for accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""### Predictions on our test set"""

test_loss, test_acc = first_model.evaluate(X_test, y_test)

print('\nTest accuracy:', test_acc)
print('\nTest loss:', test_loss)

predictions = first_model.predict(X_test)

def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(label_names[predicted_label],
                                100*np.max(predictions_array),
                                label_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

i = 3ßßßß
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions, y_test, X_test)
plt.subplot(1,2,2)
plot_value_array(i, predictions,  y_test)
plt.show()

import seaborn as sns

y = predictions[i]
x = label_names

y

sns.barplot(x=x, y=y)

