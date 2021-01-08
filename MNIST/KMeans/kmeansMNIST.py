import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import keras
import time

np.random.seed(42)

# X_digits, y_digits = datasets.load_digits(return_X_y=True)
# X_digits, y_digits = datasets.fetch_openml('mnist_784', return_X_y=True)
# X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits, random_state=42)

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

k = 100
start = time.time()

kmeans = MiniBatchKMeans(n_clusters=k, random_state=42, n_init=1).fit(X_train)
# kmeans = KMeans(n_clusters=k, random_state=42, n_init=1).fit(X_train)
y_pred_indices = kmeans.predict(X_test)

X_digits_dist = kmeans.transform(X_train)
representative_digit_idx = np.argmin(X_digits_dist, axis=0)
y_representative_digits = y_train[representative_digit_idx]
y_pred = y_representative_digits[y_pred_indices]

accuracy = sklearn.metrics.accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy} with k={k}")
print(f"Time taken: {time.time()-start}")
