import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import time
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# X_digits, y_digits = datasets.load_digits(return_X_y=True)
# X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits, random_state=42)

import keras
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

print("Data Shapes before PCA:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)

start = time.time()

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

pca = PCA(0.95)
pca.fit(X_train)

X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

print("Data Shapes after PCA:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)

k=2

knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
accuracy = knn.score(X_test, y_test)

print(f"Accuracy: {accuracy} with k={k}")
print(f"Time taken: {time.time()-start}")
