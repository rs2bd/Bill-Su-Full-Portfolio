#!/usr/bin/python

import sys
import pandas
import pickle
import scipy
import numpy
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list =  [u'poi', u'total_payments',
       u'exercised_stock_options', u'bonus', u'restricted_stock',
       u'shared_receipt_with_poi', u'total_stock_value', u'expenses',
       u'percent_messages_to_poi', u'percent_messages_from_poi'] # You will need to use more features


### Task 2: Remove outliers, invalid columns, and rows
df = pandas.DataFrame.from_dict(pandas.read_pickle("../final_project/final_project_dataset.pkl"), orient = "index")
df = df.drop(["TOTAL"])
df = df.drop(["email_address"], axis= 1)
df = df.applymap(lambda x: numpy.nan if x == "NaN" else x)
df = df.dropna(axis=1, thresh = 80)

### Create new feature(s)
# Create new feature, email_percentage
df["percent_messages_from_poi"] = df["from_poi_to_this_person"]/df["to_messages"]
df["percent_messages_to_poi"] = df["from_this_person_to_poi"]/df["from_messages"]

c_list = list(df.columns)
outlier_df = df
outliers = []
for column in c_list:
    # intropolate NAs
    df[column] = df[column].fillna(df[column].mean())
#     temp = df
    outlier_df = df[abs(df[column] - df[column].mean()) <= 6*(df[column].std())]
    if type(outliers) == type([]) :
        outliers = pandas.DataFrame(df[abs(df[column] - df[column].mean()) > 6*(df[column].std())])
    else:
        outliers = pandas.concat([outliers, df[abs(df[column] - df[column].mean()) > 6*(df[column].std())]])

outlier_labels = list(outliers.drop_duplicates().index)
outlier_index = []
for item in outlier_labels:
    outlier_index.append(df.index.get_loc(item))



# Select correct group of features for both dataframes
df = df[features_list]
no_outlier_df = outlier_df[features_list]



my_dataset = df.transpose().to_dict("dict")
no_outlier_dataset = no_outlier_df.transpose().to_dict("dict")

### Extract features and labels from dataset for local testing
no_outlier_data = featureFormat(no_outlier_dataset, features_list, sort_keys = True)
data = featureFormat(my_dataset, features_list, sort_keys = True)
kfold_labels, kfold_features = targetFeatureSplit(data)
labels, features = targetFeatureSplit(no_outlier_data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
### Due to requirenment of KFold validation, actual fitting is placed below.

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
from sklearn import feature_selection
from sklearn import cross_validation
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

from sklearn.cross_validation import KFold

# X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size= .5)
# clf = DecisionTreeClassifier()
# selector = feature_selection.SelectKBest(feature_selection.f_classif, k=4)
# X_train = selector.fit_transform(X_train, y_train)
# X_test = selector.transform(X_test)
# clf.fit(X_train, y_train)
# predicted = clf.predict(X_test)
#
# print metrics.recall_score(y_test, predicted)
# print metrics.precision_score(y_test, predicted)
# sys.exit()


#Set Final Model Parameters
parameters = {'criterion':('gini', 'entropy'), 'max_depth': (1,2,3,4)}
# parameters = {'n_estimators':(1, 10, 50, 100), 'bootstrap_features': (True, False)}

#Set Classifier
# c = BaggingClassifier()
# c = RandomForestClassifier()
c = DecisionTreeClassifier()
cv = cross_validation.StratifiedShuffleSplit(labels,n_iter = 50,random_state = 42, test_size=.1)

#Select Features
selector = feature_selection.SelectKBest(feature_selection.f_classif, k=2)

#Tune Parameters
grid = GridSearchCV(c, parameters, scoring = "f1", cv = cv)
features = selector.fit_transform(features, labels)
grid.fit(features,labels)

# This is the best classifier
clf = grid.best_estimator_

# Fit Classifier on entire dataset
clf.fit(features, labels)



#Setup KFold to validate model, notice the entire dataset was used
kf = KFold(len(my_dataset.keys()), n_folds = 5, shuffle= True)
precision = []
recall = []

i = 0
while i < 10:
    i += 1
    for train_index, test_index in kf:

        # Remove Outliers from Training, but keep them if they are in the testing set.
        for item in outlier_index:
            if item in train_index:
                train_index= numpy.delete(train_index, str(item))

        #Test and train to see model accuracy
        features_train = numpy.asarray(kfold_features)[train_index]
        features_test = numpy.asarray(kfold_features)[test_index]
        labels_train, labels_test = numpy.asarray(kfold_labels)[train_index], numpy.asarray(kfold_labels)[test_index]

        features_train = selector.fit_transform(features_train, labels_train)
        features_test = selector.transform(features_test)
        # print "score", clf.score(X_test, X_test)

        # Fit Classifier on kfold dataset
        clf.fit(features_train, labels_train)

        predicted = clf.predict(features_test)
        if metrics.precision_score(labels_test, predicted) != 0 and metrics.recall_score(labels_test, predicted) != 0:
            precision.append(metrics.precision_score(labels_test, predicted))
            recall.append(metrics.recall_score(labels_test, predicted))


print numpy.mean(precision)
print numpy.mean(recall)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)