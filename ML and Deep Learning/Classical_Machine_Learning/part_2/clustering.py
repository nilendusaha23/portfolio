#This code includes the clustering method using K-Means, Birch and Spectral Clustering
#Only the default configuration of this method has been implemented
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import accuracy_score
from itertools import cycle, islice



pd.set_option('display.max_columns', 100)
cancer_data= pd.read_csv('data.csv',  index_col= None, na_values='?')




cancer_data.drop('Unnamed: 32', axis=1 , inplace=True)
cancer_data.drop('id', axis=1 , inplace=True)

# data duplication check
cancer_data.duplicated

#print('Number of rows before discarding duplicates = %d' % (cancer_data.shape[0]))
data2 = cancer_data.drop_duplicates()
#print('Number of rows after discarding duplicates = %d' % (data2.shape[0]))

#Separate the predictors and target.
x = cancer_data.loc[: , 'radius_mean':'fractal_dimension_worst']
y_true = cancer_data.loc[:, 'diagnosis']
print("Shape of x: ", x.shape)
print("Shape of y_true: ", y_true.shape)


# Mapping Benign to 0 and Malignant to 1 
y_true = y_true.map({'M':1,'B':0})
print(y_true)


X = StandardScaler().fit_transform(x)

#####K-Means Clustering Method
print("KMeans Clustering")

#import Kmeans
from sklearn.cluster import KMeans

km = KMeans(n_clusters=2, init='k-means++', n_init=90, max_iter=200, tol=0.0001, verbose=0, algorithm='auto', random_state=None, precompute_distances='auto')
km_pred = km.fit(X) #Fitting the model
labels = km.labels_  #Getting the ground truth
y_km = km.fit_predict(X)
clusters = km.cluster_centers_

# Metrics
print('Accuracy Score: ', accuracy_score(y_true, labels))

print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(y_true, labels))
      
print("Homogeneity: %0.3f" % metrics.homogeneity_score(y_true, labels))

print("Completeness: %0.3f" % metrics.completeness_score(y_true, labels))

print("V-measure: %0.3f" % metrics.v_measure_score(y_true, labels))


# Scatter plots
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

colors = np.array(list(islice(cycle(['#FF0000', '#0000ff']),
                                      int(max(labels) + 1))))
# add black color for outliers (if any)
colors = np.append(colors, ["#000000"])

ax1.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_true])
ax1.set_title("Actual clusters")


ax2.scatter(X[y_km == 0,0], X[y_km == 0,1], s=10, color='red')
ax2.scatter(X[y_km == 1,0], X[y_km == 1,1], s=10, color='blue')
ax2.scatter(clusters[0][0], clusters[0][1],marker='*', s=100, color='black')
ax2.scatter(clusters[1][0], clusters[1][1],marker='*', s=100, color='black')
ax2.set_title("KMeans clustering plot")
plt.show()

print("END OF PART 2(clustering with K-Means)")
print("The best Clustering method is again followed in Part 3 of the assignment")
print("\n\n")
#Further comparison of the best clustering is attempted in the report


#####Birch Clustering Method
print("Birch Clustering")
#import Birch
from sklearn.cluster import Birch
from sklearn.mixture import GaussianMixture

birch = Birch(n_clusters=2, branching_factor=50, threshold=0.5, copy=True )
birch_fit = birch.fit(x) #Fitting the model
labels = birch.labels_ #Getting the ground truth
y_km = birch.fit_predict(X)


# Metrics
print('Accuracy Score: ', accuracy_score(y_true, labels))

print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(y_true, labels))
      
print("Homogeneity: %0.3f" % metrics.homogeneity_score(y_true, labels))

print("Completeness: %0.3f" % metrics.completeness_score(y_true, labels))

print("V-measure: %0.3f" % metrics.v_measure_score(y_true, labels))

# Scatter plots
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

colors = np.array(list(islice(cycle(['#0000ff', '#FF0000']),
                                      int(max(labels) + 1))))
# add black color for outliers (if any)
colors = np.append(colors, ["#000000"])

ax1.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_true])
ax1.set_title("Actual clusters")




ax2.scatter(X[y_km == 0,0], X[y_km == 0,1], s=10, color='red')
ax2.scatter(X[y_km == 1,0], X[y_km == 1,1], s=10, color='blue')

ax2.set_title("Birch clustering plot")
plt.show()
print("END OF PART 2(clustering with Birch)")
print("The best Clustering method is again followed in Part 3 of the assignment")
print("\n\n")
#Further comparison of the best clustering is attempted in the report


#####Spectral Clustering Method
print("Spectral Clustering")
#import SpectralClustering
from sklearn.cluster import SpectralClustering

spec = SpectralClustering(n_clusters=2, eigen_solver=None, n_components=None, random_state=None, n_init=10, gamma=0.7, affinity='nearest_neighbors', n_neighbors=30, eigen_tol=0.001, assign_labels='kmeans', degree=5, coef0=2, kernel_params=None, n_jobs=None)
spec_pred = spec.fit(X) #Fitting the model
labels = spec.labels_  #Getting the ground truth


# Metrics
print('Accuracy Score: ', accuracy_score(y_true, labels))

print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(y_true, labels))
      
print("Homogeneity: %0.3f" % metrics.homogeneity_score(y_true, labels))

print("Completeness: %0.3f" % metrics.completeness_score(y_true, labels))

print("V-measure: %0.3f" % metrics.v_measure_score(y_true, labels))


# Scatter plots
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                             '#f781bf', '#a65628', '#984ea3',
                                             '#999999', '#e41a1c', '#dede00']),
                                      int(max(labels) + 1))))
# add black color for outliers (if any)
colors = np.append(colors, ["#000000"])

ax1.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_true])
ax1.set_title("Actual clusters")

ax2.scatter(X[:, 0], X[:, 1], s=10, color=colors[labels])
ax2.set_title("Spectral clustering plot")
plt.show()
print("END OF PART 2(clustering with SpectralClustering)")
print("The best Clustering method is again followed in Part 3 of the assignment")
#Further comparison of the best clustering is attempted in the report
