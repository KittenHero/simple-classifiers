from argparse import ArgumentParser
from gaussian_bayes import GaussianNaiveBayes
from decision_tree import DecisionTree
from csv import reader

def parse_args():
    args = ArgumentParser()
    args.add_argument('training', type=open)
    args.add_argument('test', type=open)
    args.add_argument('model', choices=['NB', 'DT'], help='type of classifier, NB for numeric, DT for discrete')
    return args.parse_args()

def classify(model, training, test):
    if model == 'NB':
        model = GaussianNaiveBayes
    if model == 'DT':
        model = DecisionTree

    model = model(reader(training))
    return model.classify_many(*reader(test))

if __name__ == '__main__':
    for label in classify(**vars(parse_args())):
        print(label)

