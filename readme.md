Accuracy of Simple Classifiers
==============================

Classifier Accuracy
-------------------

| Numeric Data         | ZeroR     | 1R        | 1NN       | 5NN       | NB        | MLP       | SVM       | RF        | MyNB      |
|----------------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| No feature selection | 65.1042 % | 70.8333 % | 67.8385 % | 74.4792 % | 75.1302 % | 75.3906 % | 76.3021 % | 74.8698 % | xx.xxxx % |
| CFS                  | 65.1042 % | 70.8333 % | 69.0104 % | 74.4792 % | 76.3021 % | 75.7813 % | 76.6927 % | 75.9115 % | xx.xxxx % |

| Nominal Data         | DT unpruned | DT pruned |  MyDT     |
|----------------------|-------------|-----------|-----------|
| No feature selection | 75 %        | 75.3906 % | xx.xxxx % |
| CFS                  | 80.0781 %   | 79.5573 % |           |

### Decision Trees

#### Weka Unpruned DT

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
