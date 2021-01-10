import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import time

def distance(p1, p2):  # finds the squared euclidean distance between p1 and p2
    return sum((p1[i]-p2[i])**2 for i in range(len(p1)))

def findNearest(point, dict_of_points, k):
    distances = []
    for point2 in dict_of_points:
        dist = distance(point, point2)
        ind = 0
        while(ind < len(distances) and dist > distances[ind][0]):
            ind += 1
        distances.insert(ind, (dist, point2))
        
    return {(key:=distances[i][1]):dict_of_points[key] for i in range(min(k, len(distances)))}

def mode(iterable):
    iterable_counts = {x:0 for x in iterable}
    for x in iterable:
        iterable_counts[x] += 1
    return max((iterable_counts[key], key) for key in iterable_counts)[-1]
        
np.random.seed(42)

X_digits, y_digits = datasets.load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits, random_state=42)

# import keras
# (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
# X_train = X_train.reshape(X_train.shape[0], -1)
# X_test = X_test.reshape(X_test.shape[0], -1)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

k_means = 50
k_closest_means = 1 #lower --> faster; higher --> more accurate/true to KNN
k_nearest_neighbors = 1

start = time.time()
# kmeans
kmeans_model = MiniBatchKMeans(n_clusters=k_means, random_state=42, n_init=1).fit(X_train)
kmeans_y_pred = kmeans_model.labels_
kmeans_centroids = [tuple(centroid) for centroid in kmeans_model.cluster_centers_]
kmeans_info = {centroid:{} for centroid in kmeans_centroids}
for i in range(len(X_train)):
    kmeans_info[kmeans_centroids[kmeans_y_pred[i]]][tuple(X_train[i])] = int(y_train[i])
kmeans_info = {centroid:kmeans_info[centroid] for centroid in kmeans_info if kmeans_info[centroid]}
    
print("Done with kmeans. Time Taken:", time.time()-start)

y_pred = []
num_points_checked = []
for test_point in X_test:
    centroids = findNearest(test_point, kmeans_info, k_closest_means)
    all_closest_points = {point:centroids[centroid][point] for centroid in centroids for point in centroids[centroid]}
    num_points_checked.append(len(all_closest_points))
    if(len(num_points_checked) == 2000): print("2k test cases done; 1/5 done")
    k_closest_points = findNearest(test_point, all_closest_points, k_nearest_neighbors)
    labels = [k_closest_points[point] for point in k_closest_points]
    label = mode(labels)
    # print(labels, label)
    y_pred.append(label)

accuracy = sklearn.metrics.accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(f"Time Taken: {time.time()-start}")
print("Average number of points checked:", sum(num_points_checked)/len(num_points_checked))
    
    
    
    
'''
for each test point:
    find x closest means from kmeans dictionary
    find distance to every train point (squared euclidean distance) in lists from x means (use insertion sort to store)
    find k closest distances and find mode of labels
'''

