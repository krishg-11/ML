#%% Import Statements
import keras
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import time
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
tf.random.set_seed(42)

#%% Downloading Dataset and Splitting/Normalizing
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255

#%% Optional PCA and Scaler Code
print("Shape before PCA:", X_train.shape,
      X_test.shape, y_train.shape, y_test.shape)

# scaler = StandardScaler()
# scaler.fit(X_train)
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)

# pca = PCA(0.95)
# pca.fit(X_train)

# X_train = pca.transform(X_train)
# X_test = pca.transform(X_test)

print("Shape after PCA:", X_train.shape,
      X_test.shape, y_train.shape, y_test.shape)

#%% Build Model
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy",
              optimizer=keras.optimizers.SGD(lr=2e-1),
              metrics=["accuracy"])

early_stopping_cb = keras.callbacks.EarlyStopping(patience=20)
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    "my_mnist_model.h5", save_best_only=True)

#%% Train Model and Save
history = model.fit(X_train, y_train, epochs=100,
                    validation_data=(X_valid, y_valid),
                    callbacks=[early_stopping_cb, checkpoint_cb])
keras.models.save_model("my_mnist_model.h5", "my_mnist_model.h5")

#%% Test Model
model = keras.models.load_model("my_mnist_model.h5")  # rollback to best model
model.evaluate(X_test, y_test)