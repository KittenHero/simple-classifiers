---
title:	Effectiveness of Machine Learning on Predicting Diabetes
author:
	- 460251747
	- 460358275
date: 18 May 2018

geometry: margin=1in
---

Abstract
--------

The study investigated the effectiveness of common classification models on Weka
as well as our own implementation of Gaussian naive Bayes and decision tree on
predicting diabetes diagnosis.  Most algorithms have roughly the same cross-validation accuracy (~0.75),
however, decision trees showed a significant improvement after feature selection (~0.8).
The structure of these decision trees shows that glucose tolerance test,
body mass index are the most predictive factors.


Introduction
------------

Machine learning (ML) is experiencing a resurgence in the software community due to recent
increase in availability of data and computational power.  It promises solutions to high-dimensional
problem in many fiends including linguistics, robotics, analytics and medicine.  Artificial intelligence
research has yielded many classification and feature selection algorithms that can be applied for any type of data.
This study will attempt to evaluate the effectiveness of the most well known algorithms on health data and the effect
of feature selection on these algorithms.

The algorithms examined in this study are, from Weka:

1. ZeroR
2. 1R
3. 1 Nearest Neighbour
4. 5 Nearest Neighbour
5. Naive Bayes
6. Multilayer Perceptron
7. Support Vector Machine
8. Random Forest
9. Decision Tree

We also implement classifiers which have closed form evaluation (as supposed to approximated parameters) listed below:

1. Naive Bayes
2. Decision Tree

Data
----

The data used in this study comes from the National Institute of Diabetes and Digestive Kidney Diseases in the United States.
It contains 768 instances (each one representing a patient), each with eight different attributes listed below:

1. Number of times pregnant
2. Plasma glucose concentration a 2 hours in an oral glucose tolerance test
3. Diastolic blood pressure (mm Hg)
4. Triceps skin fold thickness (mm)
5. 2-Hour serum insulin (mu U/ml)
6. Body mass index (weight in kg/(height in m)^2)
7. Diabetes pedigree function
8. Age (years)

These data are preprocessed by normalisation and performing Correlation-based feature selection (CFS) in Weka.
CFS selects a subset of features with highest correlation with the predicting class and lowest correlation
to each other.  Each algorithm is then evaluated based on 10 fold cross-validation accuracy using the
normalised dataset and the CFS set.  The features selected by CFS are listed below:

1. Plasma glucose concentration a 2 hours in an oral glucose tolerance test
2. 2-Hour serum insulin (mu U/ml)
3. Body mass index (weight in kg/(height in m)^2)
4. Diabetes pedigree function
5. Age (years)

In addition, a discretised variant of the same data is used for creating decision trees.

Algorithms
----------

Our implementation of Naive Bayes assumes that the data is normally distributed for each value of the predicting class
and that the base rate for each class is the same in the training set as the testing set.  Our decision tree implementation
selects attributes based on information gain and only stops if there are no attributes left or if all the data have the
same predicting class.  Both implementation as well as the code for cross-validation will be available elsewhere.

Results and discussion
----------------------

CFS selected 5 out of the 8 attributes for predicting the class.  The discarded attribute makes intuitive sense
as pregnancy should not correlation with diabetes while blood pressure and skin fold thickness would be only
weakly correlated to diabetes and more correlated with other features such as age and body mass index.
In addition to improving classification accuracy, having a smaller set of features can make it easier to collect data
and faster to train the classifiers.


### Classifier Accuracy

| Numeric Data         | ZeroR     | 1R        | 1NN       | 5NN       | NB        | MLP       | SVM       | RF        | MyNB      |
|----------------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| No feature selection | 0.651042  | 0.708333  | 0.678385  | 0.744792  | 0.751302  | 0.753906  | 0.763021  | 0.748698  | 0.752604  |
| CFS                  | 0.651042  | 0.708333  | 0.690104  | 0.744792  | 0.763021  | 0.757813  | 0.766927  | 0.759115  | 0.768229  |

As would be expected zero rule and 1 rule are not affected by feature selection.  Zero rule isn't affected because it does not look at the test data to make its prediction.
1R does use the test data, however it only uses the attribute with the minimum error (highest correlation) which is kept by CFS.  With the exception of single nearest neighbour, most algorithm performed significantly better than 1R.
While these classifiers are really simple and fast to train, they don't do nearly as well as more sophisticated models.

1 nearest neighbour showed roughly a percent increase in accuracy after feature selection.  This is due to a decrease in distance between correlated points from lowering the dimensionality of the data.
5 nearest neighbour however did not show any increase in predictive power, since the algorithm is much more stable, being roughly 5 percent more accurate than single nearest neighbour after CFS.

Multilayer perceptron and support vector machine outperformed most other algorithms before feature selection, however CFS only
improved their performance by roughly .4 percent.  This is likely due to their sensitivity to initial parameters
and vanishing gradients.  However, SVM does perform better than MLP due to the maximisation of the decision boundary.

Random forest which builds decision trees based on random subsets of the attributes performed roughly 1 percent better after feature selection.
This is expected since the subsets of features after selection should be more correlated with the predictive class than subsets before the selection,
however the improvement is small since there aren't many attributes initially.

Naive Bayes performed nearly as well as MLP and SVM, with roughly a percent increase after feature selection.  Our implementation of Naive Bayes appears to be more accurate than Weka, however this may only be an artefact of how we handle tied probability.
In addition, naive Bayes classifiers are much faster to train and classify, requiring only linear time on the length of the input and robust to over-fitting.

| Nominal Data         | DT unpruned | DT pruned |  MyDT     |
|----------------------|-------------|-----------|-----------|
| No feature selection | 0.75        | 0.753906  | 0.821615  |
| CFS                  | 0.792471    | 0.792471  | 0.803385  |

While theoretically discretised data holds much less information than numeric data, the decision trees has overall very high predictive power and a roughly 4 percent increase after feature selection.
However our implementation, while showing the most accuracy showed a reduction in accuracy after selection.  While CFS selects the best subset of features for predicting the class, there is still
a loss of information from discarding an attribute.  Since our implementation exhausts the information entropy of the training set to build the tree, the reduction in information could lower its
predictive power.  However, this could also be interpreted as signs of over-fitting.  This likely due to our implementation using much more information from each example than
Weka, which has different method of selecting attributes and stopping condition.

The tree produced by our implementation is very similar to Weka unpruned tree, with the top two root attributes and large parts of the tree identical,
except for where our tree predicts the same class for multiple children, Weka tree would have a leaf node.  Pruning marginally improves the accuracy of the tree before feature selection and does not
affect the accuracy after selection, however, it has the advantage of being smaller and faster.

Conclusion
----------

CFS appears to improve the accuracy of prediction across types of the classifiers.  We found that decision trees have the highest cross-validation accuracy after CFS, followed closely by support vector machines and naive Bayes.  We found that the most predictive factors associated with diabetes in descending order are glucose tolerance test, body mass index, age, serum insulin and genetics.

However, this does not necessarily generalise to the general population, as the global base rate of
diabetes is much lower than the base rate in the data, due to self selection bias.  Further work could
be done on a dataset with random sample from the population, or using non-health-related data to predict
medical outcomes.


Reflection
----------

While there is a lot of excitement on complex artificial neural networks, simpler algorithms like naive Bayes and decision tree remains competitive and may even dominate in performance.
Likewise, having more information may not necessarily improve a decision than just having the most relevant information.  This can be countered by feature selection.

Appendix
--------

### Weka Unpruned DT

```
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|   |    Triceps skin fold thickness = high
|   |   |   Number of times pregnant = low
|   |   |   |    Diabetes pedigree function = high
|   |   |   |   |    Age = high: yes (16.0/5.0)
|   |   |   |   |    Age = low
|   |   |   |   |   |    Diastolic blood pressure = high: yes (11.0/5.0)
|   |   |   |   |   |    Diastolic blood pressure = low: no (5.0/2.0)
|   |   |   |    Diabetes pedigree function = low
|   |   |   |   |    Diastolic blood pressure = high: no (43.0/19.0)
|   |   |   |   |    Diastolic blood pressure = low: yes (10.0/4.0)
|   |   |   Number of times pregnant = high
|   |   |   |    Diastolic blood pressure = high: yes (29.0/8.0)
|   |   |   |    Diastolic blood pressure = low
|   |   |   |   |    Diabetes pedigree function = high: no (2.0)
|   |   |   |   |    Diabetes pedigree function = low: yes (3.0)
|   |    Triceps skin fold thickness = low: no (13.0/4.0)
|    Body mass index = low: no (29.0/4.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low
|    Body mass index = high
|   |    2-Hour serum insulin = high
|   |   |    Age = high
|   |   |   |    Diabetes pedigree function = high: yes (7.0/3.0)
|   |   |   |    Diabetes pedigree function = low: no (28.0/4.0)
|   |   |    Age = low: no (43.0/4.0)
|   |    2-Hour serum insulin = low: no (48.0/2.0)
|    Body mass index = low: no (66.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = very high
|    2-Hour serum insulin = high
|   |    Body mass index = high: yes (103.0/16.0)
|   |    Body mass index = low
|   |   |    Age = high: yes (12.0/3.0)
|   |   |    Age = low: no (4.0/1.0)
|    2-Hour serum insulin = low: no (3.0/1.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    Age = high
|   |    2-Hour serum insulin = high
|   |   |    Body mass index = high
|   |   |   |    Diabetes pedigree function = high: yes (37.0/10.0)
|   |   |   |    Diabetes pedigree function = low
|   |   |   |   |    Diastolic blood pressure = high: no (57.0/24.0)
|   |   |   |   |    Diastolic blood pressure = low
|   |   |   |   |   |    Triceps skin fold thickness = high: yes (15.0/7.0)
|   |   |   |   |   |    Triceps skin fold thickness = low: no (3.0/1.0)
|   |   |    Body mass index = low: no (27.0/3.0)
|   |    2-Hour serum insulin = low: no (8.0)
|    Age = low
|   |    Body mass index = high
|   |   |   Number of times pregnant = low
|   |   |   |    Triceps skin fold thickness = high
|   |   |   |   |    Diabetes pedigree function = high
|   |   |   |   |   |    Diastolic blood pressure = high: no (17.0/2.0)
|   |   |   |   |   |    Diastolic blood pressure = low: yes (7.0/3.0)
|   |   |   |   |    Diabetes pedigree function = low: no (54.0/8.0)
|   |   |   |    Triceps skin fold thickness = low: no (24.0/1.0)
|   |   |   Number of times pregnant = high: yes (2.0/1.0)
|   |    Body mass index = low: no (42.0/1.0)
```

### Weka Unpruned DT CFS

```
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|   |    Age = high: yes (82.0/31.0)
|   |    Age = low: no (50.0/21.0)
|    Body mass index = low: no (29.0/4.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low
|    Body mass index = high
|   |    2-Hour serum insulin = high
|   |   |    Age = high
|   |   |   |    Diabetes pedigree function = high: yes (7.0/3.0)
|   |   |   |    Diabetes pedigree function = low: no (28.0/4.0)
|   |   |    Age = low: no (43.0/4.0)
|   |    2-Hour serum insulin = low: no (48.0/2.0)
|    Body mass index = low: no (66.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = very high
|    2-Hour serum insulin = high
|   |    Body mass index = high: yes (103.0/16.0)
|   |    Body mass index = low
|   |   |    Age = high: yes (12.0/3.0)
|   |   |    Age = low: no (4.0/1.0)
|    2-Hour serum insulin = low: no (3.0/1.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    Age = high
|   |    Body mass index = high
|   |   |    Diabetes pedigree function = high: yes (37.0/10.0)
|   |   |    Diabetes pedigree function = low: no (80.0/33.0)
|   |    Body mass index = low: no (30.0/3.0)
|    Age = low: no (146.0/17.0)
```

### Weka Pruned DT

```
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|   |    Triceps skin fold thickness = high: yes (119.0/51.0)
|   |    Triceps skin fold thickness = low: no (13.0/4.0)
|    Body mass index = low: no (29.0/4.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low: no (192.0/14.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = very high: yes (122.0/24.0)
 Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    Age = high
|   |    Body mass index = high
|   |   |    Diabetes pedigree function = high: yes (37.0/10.0)
|   |   |    Diabetes pedigree function = low: no (80.0/33.0)
|   |    Body mass index = low: no (30.0/3.0)
|    Age = low: no (146.0/17.0)
```

### Weka Pruned DT CFS

```
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|   |    Age = high: yes (82.0/31.0)
|   |    Age = low: no (50.0/21.0)
|    Body mass index = low: no (29.0/4.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low: no (192.0/14.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = very high: yes (122.0/24.0)
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    Age = high
|   |    Body mass index = high
|   |   |    Diabetes pedigree function = high: yes (37.0/10.0)
|   |   |    Diabetes pedigree function = low: no (80.0/33.0)
|   |    Body mass index = low: no (30.0/3.0)
|    Age = low: no (146.0/17.0)
```

### MyDT

```
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|    |    age = high
|    |    |    Diabetes pedigree function = high
|    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    Number of times pregnant = high
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    |    |    2-Hour serum insulin = low: yes
|    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    Number of times pregnant = high: no
|    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    Diabetes pedigree function = low
|    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    Number of times pregnant = high: yes
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    Number of times pregnant = high: yes
|    |    |    |    |    |    |    Number of times pregnant = low: yes
|    |    |    |    |    Triceps skin fold thickness = low
|    |    |    |    |    |    Number of times pregnant = high: no
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Diastolic blood pressure = high: yes
|    |    |    |    |    |    |    Diastolic blood pressure = low: no
|    |    |    |    2-Hour serum insulin = low: yes
|    |    age = low
|    |    |    Triceps skin fold thickness = high
|    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    Triceps skin fold thickness = low
|    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    |    |    Number of times pregnant = low: yes
|    |    |    |    |    |    Diabetes pedigree function = low: no
|    |    |    |    |    2-Hour serum insulin = low: no
|    Body mass index = low
|    |    Triceps skin fold thickness = high
|    |    |    2-Hour serum insulin = high
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    age = high
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    |    Diastolic blood pressure = low: no
|    |    |    |    |    age = low
|    |    |    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    Number of times pregnant = low: yes
|    |    |    2-Hour serum insulin = low
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low: no
|    |    Triceps skin fold thickness = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low
|    Body mass index = high
|    |    2-Hour serum insulin = high
|    |    |    age = high
|    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    Number of times pregnant = high
|    |    |    |    |    |    |    Triceps skin fold thickness = high: yes
|    |    |    |    |    |    |    Triceps skin fold thickness = low: no
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Triceps skin fold thickness = high: no
|    |    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    |    Diastolic blood pressure = low: yes
|    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    Number of times pregnant = high
|    |    |    |    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    |    |    |    Diastolic blood pressure = low: no
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    |    |    |    Diastolic blood pressure = low: no
|    |    |    |    |    Triceps skin fold thickness = low: no
|    |    |    age = low
|    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    Triceps skin fold thickness = low: no
|    |    2-Hour serum insulin = low
|    |    |    Diastolic blood pressure = high
|    |    |    |    age = high: no
|    |    |    |    age = low
|    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    Triceps skin fold thickness = low: no
|    |    |    Diastolic blood pressure = low: no
|    Body mass index = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    age = high
|    |    Body mass index = high
|    |    |    Diabetes pedigree function = high
|    |    |    |    Number of times pregnant = high: yes
|    |    |    |    Number of times pregnant = low
|    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    Diabetes pedigree function = low
|    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    Number of times pregnant = high
|    |    |    |    |    |    |    Triceps skin fold thickness = high: no
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Triceps skin fold thickness = high: no
|    |    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    Number of times pregnant = high: yes
|    |    |    |    |    |    |    Number of times pregnant = low: yes
|    |    |    |    |    |    Triceps skin fold thickness = low
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    2-Hour serum insulin = low: no
|    |    Body mass index = low
|    |    |    Diastolic blood pressure = high
|    |    |    |    Number of times pregnant = high: no
|    |    |    |    Number of times pregnant = low
|    |    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    |    |    Triceps skin fold thickness = low: no
|    |    |    Diastolic blood pressure = low
|    |    |    |    Number of times pregnant = high: yes
|    |    |    |    Number of times pregnant = low
|    |    |    |    |    Triceps skin fold thickness = high: no
|    |    |    |    |    Triceps skin fold thickness = low
|    |    |    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    |    |    Diabetes pedigree function = high: no
|    age = low
|    |    Body mass index = high
|    |    |    Triceps skin fold thickness = high
|    |    |    |    Number of times pregnant = high
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    |    |    Diabetes pedigree function = low: yes
|    |    |    |    Number of times pregnant = low
|    |    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    |    |    |    2-Hour serum insulin = low: no
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    |    |    |    2-Hour serum insulin = low: yes
|    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    |    |    |    2-Hour serum insulin = low: no
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    |    |    |    2-Hour serum insulin = low: no
|    |    |    Triceps skin fold thickness = low
|    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    2-Hour serum insulin = high
|    |    |    |    |    |    |    Number of times pregnant = low: no
|    |    |    |    |    |    2-Hour serum insulin = low: no
|    |    |    |    Diabetes pedigree function = low: no
|    |    Body mass index = low
|    |    |    Diabetes pedigree function = high
|    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    2-Hour serum insulin = low
|    |    |    |    |    Diastolic blood pressure = high: no
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    Diabetes pedigree function = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = very high
|    2-Hour serum insulin = high
|    |    Body mass index = high
|    |    |    Number of times pregnant = high
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    age = high: yes
|    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    age = high: yes
|    |    |    Number of times pregnant = low
|    |    |    |    age = high
|    |    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    Diastolic blood pressure = high: yes
|    |    |    |    |    |    |    Diastolic blood pressure = low: yes
|    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    Triceps skin fold thickness = high: yes
|    |    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    Triceps skin fold thickness = high: yes
|    |    |    |    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    |    age = low
|    |    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    |    Diabetes pedigree function = low
|    |    |    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    |    |    Diastolic blood pressure = high: yes
|    |    |    |    |    |    |    Diastolic blood pressure = low: yes
|    |    |    |    |    |    Triceps skin fold thickness = low
|    |    |    |    |    |    |    Diastolic blood pressure = high: yes
|    |    |    |    |    |    |    Diastolic blood pressure = low: no
|    |    Body mass index = low
|    |    |    age = high
|    |    |    |    Triceps skin fold thickness = high
|    |    |    |    |    Number of times pregnant = high
|    |    |    |    |    |    Diabetes pedigree function = high
|    |    |    |    |    |    |    Diastolic blood pressure = high: yes
|    |    |    |    |    |    |    Diastolic blood pressure = low: yes
|    |    |    |    |    |    Diabetes pedigree function = low: yes
|    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    |    |    Diabetes pedigree function = low: yes
|    |    |    |    |    |    Diastolic blood pressure = low
|    |    |    |    |    |    |    Diabetes pedigree function = low: yes
|    |    |    |    Triceps skin fold thickness = low: yes
|    |    |    age = low
|    |    |    |    Diastolic blood pressure = high
|    |    |    |    |    Triceps skin fold thickness = high: no
|    |    |    |    |    Triceps skin fold thickness = low
|    |    |    |    |    |    Number of times pregnant = low
|    |    |    |    |    |    |    Diabetes pedigree function = low: yes
|    |    |    |    Diastolic blood pressure = low: no
|    2-Hour serum insulin = low
|    |    Diabetes pedigree function = high: yes
|    |    Diabetes pedigree function = low: no
```

### MyDT - CFS
```
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = 'very high'
|    2-Hour serum insulin = high
|    |    Body mass index = high
|    |    |    Age = high
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low: yes
|    |    |    Age = low
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low: yes
|    |    Body mass index = low
|    |    |    Age = high
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low: yes
|    |    |    Age = low
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low: no
|    2-Hour serum insulin = low
|    |    Diabetes pedigree function = high: yes
|    |    Diabetes pedigree function = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = high
|    Body mass index = high
|    |    Age = high
|    |    |    Diabetes pedigree function = high
|    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    2-Hour serum insulin = low: yes
|    |    |    Diabetes pedigree function = low
|    |    |    |    2-Hour serum insulin = high: yes
|    |    |    |    2-Hour serum insulin = low: yes
|    |    Age = low
|    |    |    2-Hour serum insulin = high
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low: no
|    |    |    2-Hour serum insulin = low: no
|    Body mass index = low
|    |    2-Hour serum insulin = high
|    |    |    Diabetes pedigree function = high: no
|    |    |    Diabetes pedigree function = low
|    |    |    |    Age = high: no
|    |    |    |    Age = low: no
|    |    2-Hour serum insulin = low
|    |    |    Diabetes pedigree function = high
|    |    |    |    Age = high: yes
|    |    |    |    Age = low: no
|    |    |    Diabetes pedigree function = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = low
|    Body mass index = high
|    |    2-Hour serum insulin = high
|    |    |    Age = high
|    |    |    |    Diabetes pedigree function = high: yes
|    |    |    |    Diabetes pedigree function = low: no
|    |    |    Age = low
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low: no
|    |    2-Hour serum insulin = low
|    |    |    Age = high: no
|    |    |    Age = low
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low: no
|    Body mass index = low: no
Plasma glucose concentration a 2 hours in an oral glucose tolerance test = medium
|    Age = high
|    |    Body mass index = high
|    |    |    Diabetes pedigree function = high
|    |    |    |    2-Hour serum insulin = high: yes
|    |    |    Diabetes pedigree function = low
|    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    2-Hour serum insulin = low: no
|    |    Body mass index = low
|    |    |    2-Hour serum insulin = high
|    |    |    |    Diabetes pedigree function = high: no
|    |    |    |    Diabetes pedigree function = low: no
|    |    |    2-Hour serum insulin = low: no
|    Age = low
|    |    Body mass index = high
|    |    |    Diabetes pedigree function = high
|    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    2-Hour serum insulin = low: no
|    |    |    Diabetes pedigree function = low
|    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    2-Hour serum insulin = low: no
|    |    Body mass index = low
|    |    |    Diabetes pedigree function = high
|    |    |    |    2-Hour serum insulin = high: no
|    |    |    |    2-Hour serum insulin = low: no
|    |    |    Diabetes pedigree function = low: no
```
