from fold_data import stratifold, partition_by_class
from gaussian_bayes import GaussianNaiveBayes
from decision_tree import DecisionTree
from csv import reader
from itertools import chain
from functools import partial


def cross_validatation_accuracy(n_folds, data, model):
    '''calculates the cross validation of the model
    calling model(data) musts return an object with the .classify method
    '''
    folds = stratifold(n_folds, *partition_by_class(data))
    correct = 0
    total = 0
    for i in range(n_folds):
        test_data = folds[i]
        train_data = chain(*folds[:i], *folds[i:])
        classifier = model(train_data)
        total += len(test_data)
        correct += sum(p[-1] == classifier.classify(p[:-1]) for p in test_data)
    return correct / total

if __name__ == '__main__':
    numeric = reader(open('pima.csv'))
    numeric_CFS = reader(open('pima-CFS.csv'))
    discrete = reader(open('pima-discretised.csv'))
    discrete_CFS = reader(open('pima-discretised-CFS.csv'))

    nb_acc = partial(cross_validatation_accuracy, 10, model=GaussianNaiveBayes)
    dt_acc = partial(cross_validatation_accuracy, 10, model=DecisionTree)
    print('NB', nb_acc(numeric))
    print('NB-CFS', nb_acc(numeric_CFS))
    print('DT', dt_acc(discrete))
    print('DT-CFS', dt_acc(discrete_CFS))
