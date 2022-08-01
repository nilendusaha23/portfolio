#This code includes the classification method using SVM alongwith the Test-Train Split
#Only the default configuration of this method has been implemented
#To maintain the ethics of the pipeline,the ground truth from the best configuration Spectral Clustering is chosen. 


from sklearn.model_selection import train_test_split # to split the data into two parts
from sklearn import svm # for Support Vector Machine
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics # for the check the error and accuracy of the model
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import accuracy_score
from itertools import cycle, islice
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import hypertools as hyp 


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

#import SpectralClustering
from sklearn.cluster import SpectralClustering


spec = SpectralClustering(n_clusters=2, eigen_solver=None, n_components=None, random_state=None, n_init=10, gamma=0.7, affinity='nearest_neighbors', n_neighbors=30, eigen_tol=0.001, assign_labels='kmeans', degree=5, coef0=2, kernel_params=None, n_jobs=None)

spec_pred = spec.fit(X) #Fitting the model
labels = spec.labels_  #Getting the ground truth




###########################################################Classification using Test-Train Split



# Splitting the dataset into the Training set and Test set

X_train, X_test, y_train, y_test = train_test_split(x, labels, test_size = 0.30, random_state = 0)  

#Feature Scaling

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


###########################################################Classification using SVM

#Using SVC method of svm class to use Support Vector Machine Algorithm
from sklearn.svm import SVC
classifier = SVC(C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)    #############################################

classifier.fit(X_train, y_train)

#Prediction on test

y_pred = classifier.predict(X_test)

#predicting with probability attribute
print(classifier.predict_proba(X_test)[:,1])


#Random Prediction from test set
print(classifier.predict([X_test[10]]))      # If both the numbers match then prediction is correct
print(y_test[10])
#Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

#################Accuracy Score
#importing Score Libraries
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score, roc_curve

print("Metrics for SVM classifier")
print("accuracy score is: ",accuracy_score(y_test, y_pred))
print("balanced accuracy score is: ",balanced_accuracy_score(y_test, y_pred))
print("F1 -- score is: ",f1_score(y_test, y_pred, average='micro'))
print("Recall score is: ",recall_score(y_test, y_pred, average='macro'))
print("Precision score is: ",precision_score(y_test, y_pred, average='macro'))



import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,roc_auc_score

fpr, tpr, thresholds = roc_curve(y_test, classifier.predict_proba(X_test)[:,1],drop_intermediate=False)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC curve for breast cancer classifier(SVM)')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.plot(fpr, tpr,color='red',lw=5)
plt.show()


print("ROC AUC Score: \n")
print(roc_auc_score(y_test, classifier.predict_proba(X_test)[:,1]))

    
print("END OF PART 3(classification with SVM using Test-Train Split)")
print("\n\n")
#Further comparison of the best Classifier is attempted in the report

#########################################################Classification using AdaBoost



#Using AdaBoost Classifier

classifier_ada = AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1.0, algorithm='SAMME.R', random_state=None)    #############################################

classifier_ada.fit(X_train, y_train)

#Prediction on test

y_pred = classifier_ada.predict(X_test)

#predicting with probability attribute
print(classifier_ada.predict_proba(X_test)[:,1])


#Random Prediction from test set
print(classifier_ada.predict([X_test[10]]))      # If both the numbers match then prediction is correct
print(y_test[10])
#Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

#################Accuracy Score
#importing Score Libraries
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score, roc_curve

print("Metrics for AdaBoost classifier")
print("accuracy score is: ",accuracy_score(y_test, y_pred))
print("balanced accuracy score is: ",balanced_accuracy_score(y_test, y_pred))
print("F1 -- score is: ",f1_score(y_test, y_pred, average='micro'))
print("Recall score is: ",recall_score(y_test, y_pred, average='macro'))
print("Precision score is: ",precision_score(y_test, y_pred, average='macro'))



import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,roc_auc_score

fpr, tpr, thresholds = roc_curve(y_test, classifier_ada.predict_proba(X_test)[:,1],drop_intermediate=False)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC curve for breast cancer classifier(AdaBoost)')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.plot(fpr, tpr,color='red',lw=5)
plt.show()


print("ROC AUC Score: \n")
print(roc_auc_score(y_test, classifier_ada.predict_proba(X_test)[:,1]))

    
print("END OF PART 3(classification with Adaboost using Test-Train Split)")
print("\n\n")
#Further comparison of the best Classifier is attempted in the report


#####################################################Classification using GaussianNB



#Using GaussianNB Classifier

classifier_nb = GaussianNB()    #############################################

classifier_nb.fit(X_train, y_train)

#Prediction on test

y_pred = classifier_nb.predict(X_test)

#predicting with probability attribute
print(classifier_nb.predict_proba(X_test)[:,1])


#Random Prediction from test set
print(classifier_nb.predict([X_test[10]]))      # If both the numbers match then prediction is correct
print(y_test[10])
#Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

#################Accuracy Score
#importing Score Libraries
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score, roc_curve

print("Metrics for Gaussian NB classifier")
print("accuracy score is: ",accuracy_score(y_test, y_pred))
print("balanced accuracy score is: ",balanced_accuracy_score(y_test, y_pred))
print("F1 -- score is: ",f1_score(y_test, y_pred, average='micro'))
print("Recall score is: ",recall_score(y_test, y_pred, average='macro'))
print("Precision score is: ",precision_score(y_test, y_pred, average='macro'))



import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,roc_auc_score

fpr, tpr, thresholds = roc_curve(y_test, classifier_nb.predict_proba(X_test)[:,1],drop_intermediate=False)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC curve for breast cancer classifier(Gaussian NB)')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.plot(fpr, tpr,color='red',lw=5)
plt.show()


print("ROC AUC Score: \n")
print(roc_auc_score(y_test, classifier_nb.predict_proba(X_test)[:,1]))

    
print("END OF PART 3(classification with GaussianNB using Test-Train Split)")
print("\n\n")
#Further comparison of the best Classifier is attempted in the report


###########################################################Classification using K-Folds Split
print("Classification using K-Folds")
print("\n\n")



from sklearn.model_selection import KFold, cross_val_score
from statistics import mean 


#Creating functions for calculating the scores for each fold evaluation
def get_score(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)
    
def get_bal_acc(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return balanced_accuracy_score(y_test, y_pred)

def get_f1score(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return f1_score(y_test, y_pred)

def get_recall(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return recall_score(y_test, y_pred)

def get_precision(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return precision_score(y_test, y_pred)
    
def get_roc(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    return roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
    
def get_pred(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    return model.predict(X_test)

#Setting the number of folds    
from sklearn.model_selection import StratifiedKFold
kf = KFold(n_splits=10,shuffle=False)
kf.split(X)


######################################################Classification using SVM
print("Classification using SVM")
#Empty Lists for storing the scores
acc_svm = []
bal_svm = []
f1_svm = []
recall_svm = []
precision_svm = []
roc_auc_svm = []
print("\n\n")
print("Printing all the confusion matrices")

for train_index, test_index in kf.split(X):
	# Split train-test
    X_train, X_test = x.iloc[train_index], x.iloc[test_index]
    #print(len(X_train))
    y_train, y_test = labels[train_index], labels[test_index]
    
    model_configue = SVC(C=0.5, kernel='rbf', degree=2, gamma='scale', coef0=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)  
    
    acc_svm.append(get_score(model_configue, X_train, X_test, y_train, y_test))
    bal_svm.append(get_bal_acc(model_configue, X_train, X_test, y_train, y_test))
    f1_svm.append(get_f1score(model_configue, X_train, X_test, y_train, y_test))
    recall_svm.append(get_recall(model_configue, X_train, X_test, y_train, y_test))
    precision_svm.append(get_precision(model_configue, X_train, X_test, y_train, y_test))
    roc_auc_svm.append(get_roc(model_configue, X_train, X_test, y_train, y_test))
    y_pred = get_pred(model_configue, X_train, X_test, y_train, y_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print("\n\n")

print("Accuracy")
print(acc_svm)
average = mean(acc_svm)
print("Avg. accuracy: ", average)
print("\n\n")

print("Balanced Accuracy")
print(bal_svm)
bal_svm_average = mean(bal_svm)
print("Avg. Balanced accuracy: ", bal_svm_average)
print("\n\n")

print("F1 Score")
print(f1_svm)
f1_svm_average = mean(f1_svm)
print("Avg. F1 Score: ", f1_svm_average)
print("\n\n")

print("Recall")
print(recall_svm)
recall_svm_average = mean(recall_svm)
print("Avg. Recall: ", recall_svm_average)
print("\n\n")

print("Precision")
print(precision_svm)
precision_svm_average = mean(precision_svm)
print("Avg. Precision: ", precision_svm_average)
print("\n\n")

print("ROC")
print(roc_auc_svm)
roc_svm_average = mean(roc_auc_svm)
print("Avg. ROC: ", roc_svm_average)
print("\n\n")

print("done")

print("END OF PART 3(classification with SVM using K-Folds Split)")
print("\n\n")
#Further comparison of the best Classifier is attempted in the report

#########################################################Classification using AdaBoost

print("Classification using AdaBoost")
#Empty Lists for storing the scores
acc_ada = []
bal_ada = []
f1_ada = []
recall_ada = []
precision_ada = []
roc_auc_ada = []
print("\n\n")
print("Printing all the confusion matrices")

for train_index, test_index in kf.split(X):
	# Split train-test
    X_train, X_test = x.iloc[train_index], x.iloc[test_index]
    #print(len(X_train))
    y_train, y_test = labels[train_index], labels[test_index]
    
    model_configue = AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1.0, algorithm='SAMME.R', random_state=None)  
    
    acc_ada.append(get_score(model_configue, X_train, X_test, y_train, y_test))
    bal_ada.append(get_bal_acc(model_configue, X_train, X_test, y_train, y_test))
    f1_ada.append(get_f1score(model_configue, X_train, X_test, y_train, y_test))
    recall_ada.append(get_recall(model_configue, X_train, X_test, y_train, y_test))
    precision_ada.append(get_precision(model_configue, X_train, X_test, y_train, y_test))
    roc_auc_ada.append(get_roc(model_configue, X_train, X_test, y_train, y_test))
    y_pred = get_pred(model_configue, X_train, X_test, y_train, y_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print("\n\n")

print("Accuracy")
print(acc_ada)
average = mean(acc_ada)
print("Avg. accuracy: ", average)
print("\n\n")

print("Balanced Accuracy")
print(bal_ada)
bal_ada_average = mean(bal_ada)
print("Avg. Balanced accuracy: ", bal_ada_average)
print("\n\n")

print("F1 Score")
print(f1_ada)
f1_ada_average = mean(f1_ada)
print("Avg. F1 Score: ", f1_ada_average)
print("\n\n")

print("Recall")
print(recall_ada)
recall_ada_average = mean(recall_ada)
print("Avg. Recall: ", recall_ada_average)
print("\n\n")

print("Precision")
print(precision_ada)
precision_ada_average = mean(precision_ada)
print("Avg. Precision: ", precision_ada_average)
print("\n\n")

print("ROC")
print(roc_auc_ada)
roc_ada_average = mean(roc_auc_ada)
print("Avg. ROC: ", roc_ada_average)
print("\n\n")
print("done")

print("END OF PART 3(classification with SVM using K-Folds Split)")
print("\n\n")
#Further comparison of the best Classifier is attempted in the report

#########################################################Classification using Gaussian NB
print("Classification using Gaussian NB")
#Empty Lists for storing the scores
acc_nb = []
bal_nb = []
f1_nb = []
recall_nb = []
precision_nb = []
roc_auc_nb = []
print("\n\n")
print("Printing all the confusion matrices")

for train_index, test_index in kf.split(X):
	# Split train-test
    X_train, X_test = x.iloc[train_index], x.iloc[test_index]
    #print(len(X_train))
    y_train, y_test = labels[train_index], labels[test_index]
    
    model_configue = GaussianNB() 
    
    acc_nb.append(get_score(model_configue, X_train, X_test, y_train, y_test))
    bal_nb.append(get_bal_acc(model_configue, X_train, X_test, y_train, y_test))
    f1_nb.append(get_f1score(model_configue, X_train, X_test, y_train, y_test))
    recall_nb.append(get_recall(model_configue, X_train, X_test, y_train, y_test))
    precision_nb.append(get_precision(model_configue, X_train, X_test, y_train, y_test))
    roc_auc_nb.append(get_roc(model_configue, X_train, X_test, y_train, y_test))
    y_pred = get_pred(model_configue, X_train, X_test, y_train, y_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print("\n\n")

print("Accuracy")
print(acc_nb)
average = mean(acc_nb)
print("Avg. accuracy: ", average)
print("\n\n")

print("Balanced Accuracy")
print(bal_nb)
bal_nb_average = mean(bal_nb)
print("Avg. Balanced accuracy: ", bal_nb_average)
print("\n\n")

print("F1 Score")
print(f1_nb)
f1_nb_average = mean(f1_nb)
print("Avg. F1 Score: ", f1_nb_average)
print("\n\n")

print("Recall")
print(recall_nb)
recall_nb_average = mean(recall_nb)
print("Avg. Recall: ", recall_nb_average)
print("\n\n")

print("Precision")
print(precision_nb)
precision_nb_average = mean(precision_nb)
print("Avg. Precision: ", precision_nb_average)
print("\n\n")

print("ROC")
print(roc_auc_nb)
roc_nb_average = mean(roc_auc_nb)
print("Avg. ROC: ", roc_nb_average)
print("\n\n")
print("done")

print("END OF PART 3(classification with Gaussian NB using K-Folds Split)")
#Further comparison of the best Classifier is attempted in the report



