'''
This module contains the GaussianNaiveBayes class
for classifying data with numeric attributes
'''
import math
import sys
import statistics as stat
from functools import reduce
from collections import OrderedDict, defaultdict
from itertools import groupby
from operator import itemgetter, mul
from pprint import pformat, pprint

class GaussianModel:
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    @classmethod
    def from_data(cls, data):
        return cls(stat.mean(data), stat.variance(data))

    def probability(self, x):
        return self.gaussian(x, self.mean, self.variance)

    @staticmethod
    def gaussian(x, m, v):
        'computes the gaussian at x parameterised by the mean and variance'
        return math.exp( -(x - m)**2 / (2*v) ) / math.sqrt( 2*math.pi*v )

    def __repr__(self):
        return '{cls}(mean={m}, variance={v})'.format(cls=self.__class__.__name__, m=self.mean, v=self.variance)


class GaussianNaiveBayes:
    def __init__(self, data):
        # seperate the data based on key
        # groupby requires data to be sorted like uniq
        # sorting in reverse puts yes before no, which is how we will break ties
        class_attr = itemgetter(-1)
        data = sorted(data, reverse=1, key=class_attr)

        self.sample_size = len(data)
        self.num_attr = len(data[0]) - 1 # the class does not count as an attr
        # target machine runs 3.5 which does not have ordered dict by default
        classes = OrderedDict(
            # here we map the data to floats and discard the class
            (key, [list(map(float, p[:-1])) for p in points])
            for key, points in groupby(data, class_attr)
        )

        self.model = OrderedDict()
        self.class_size = {}

        for label, data in classes.items():
            self.class_size[label] = len(data)
            self.model[label] = [None] * self.num_attr

            for i in range(self.num_attr):
                # extract the ith attribute
                attr = list(map(itemgetter(i), data))
                # store the model on the class
                self.model[label][i] = GaussianModel.from_data(attr)

    def classify(self, p):
        'classify the point with the from known data'
        assert(len(p) == self.num_attr)
        def rel_pr(label):
            return reduce(
                mul,
                # likelihood
                (model.probability( float(p[attr]) ) for attr, model in enumerate(self.model[label])),
                # prior
                self.class_size[label] / self.sample_size
            )
        return max(self.model, key=rel_pr)

    def classify_many(self, *points):
        return map(self.classify, points)

    def __repr__(self):
        return '{}(\nclasses={}\n)'.format(self.__class__.__name__, pformat(dict(self.model.items())))


if __name__ == '__main__':
    from argparse import ArgumentParser
    from csv import reader

    arg = ArgumentParser()
    arg.add_argument('datafile', type=open, help='CSV file containing numeric attributes and a class to train the model')
    pprint(GaussianNaiveBayes(reader(arg.parse_args().datafile)))
