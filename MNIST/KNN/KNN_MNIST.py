import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import time
import keras

np.random.seed(42)

# X_digits, y_digits = datasets.load_digits(return_X_y=True)
# X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits, random_state=42)

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# for k in range(1,100):
k=2
start = time.time()

knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
print('finished training')
# y_pred = knn.predict(X_test)
# accuracy = sklearn.metrics.accuracy_score(y_test, y_pred)
accuracy = knn.score(X_test, y_test)

print(f"Accuracy: {accuracy} with k={k}")
print(f"Time taken: {time.time()-start}")
