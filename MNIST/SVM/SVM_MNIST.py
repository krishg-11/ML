import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.svm import SVC
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

print("Shape before PCA:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

pca = PCA(0.95)
pca.fit(X_train)

X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

print("Shape after PCA:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)

start = time.time()

svm = SVC().fit(X_train, y_train)
accuracy = svm.score(X_test, y_test)

print(f"Accuracy: {accuracy}")
print(f"Time taken: {time.time()-start}")

'''
Mini dataset w/o PCA:
Accuracy: 0.9866666666666667
Time taken: 0.20024824142456055

Mini dataset w/ PCA:
Accuracy: 0.9822222222222222
Time taken: 0.1590561866760254

Full dataset w/ PCA:

'''
