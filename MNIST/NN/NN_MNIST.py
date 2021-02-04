#%% Import Statements
import keras
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import time

np.random.seed(42)
tf.random.set_seed(42)

#%% Downloading Dataset and Splitting/Normalizing
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()
print(X_train_full.shape, y_train_full.shape, X_test.shape, y_test.shape)
X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255

#%% Build Model
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy',
              optimizer=keras.optimizers.SGD(lr=2e-1),
              metrics=['accuracy'])

early_stopping_cb = keras.callbacks.EarlyStopping(patience=20)
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    'my_mnist_model.h5', save_best_only=True)

#%% Train Model and Save
start = time.time()
history = model.fit(X_train, y_train, epochs=100,
                    validation_data=(X_valid, y_valid),
                    callbacks=[early_stopping_cb, checkpoint_cb])
print('Time taken to train:', time.time()-start)
model.save('my_mnist_model.h5')

#%% Test Model
model = keras.models.load_model('my_mnist_model.h5')  # rollback to best model
model.evaluate(X_test, y_test)
# %%
'''
Training Time: ~300 seconds
Accuracy: 0.9843

23 epochs
'''
