'''This module contains the DecisionTree class
An unpruned decision tree implementation with split based on information gain
'''
import math
from operator import itemgetter
from collections import OrderedDict
from itertools import groupby

def mode(data):
    freq = OrderedDict()
    for p in data:
        freq[p] = freq.get(p, 0) + 1
    return max(freq, key=freq.get)

def entropy(data):
    '''calculate the entropy of the data
    this function requires the data to be sorted
    '''
    total = len(data)
    entropy = 0
    for k, subgroup in groupby(data, itemgetter(-1)):
        subgroup = list(subgroup)
        size = len(subgroup)
        entropy += size * math.log2(total / size)
    return entropy / total

def split_entropy(attr, data):
    data = sorted(data, key=attr)
    total = len(data)
    s_entropy = 0
    for _, subgroup in groupby(data, attr):
        data = sorted(subgroup, key=itemgetter(-1))
        s_entropy += len(data) / total * entropy(data)
    return s_entropy

class LeafNode:
    def __init__(self, label):
        self.label = label

    def classify(self, point):
        return self.label

class InnerNode:
    def __init__(self, attr, default):
        self.attr = attr
        self.default = LeafNode(default)
        self.children = {}

    def classify(self, point):
        return self.children.get(point[self.attr], self.default).classify(point)

def strfy_node(node, depth=0, base=''):
    if isinstance(node, LeafNode):
        return '{}: {}'.format(base, node.label)
    padding = '|    '*depth
    depth += 1
    return '{}\n{}'.format(
        base,
        '\n'.join(
            strfy_node(child, depth, '{}{} = {}'.format(padding, node.attr, key))
            for key, child in node.children.items()
        )
    )

class DecisionTree:
    def __init__(self, data):
        class_attr = itemgetter(-1)
        # reversing causes yes to appear before no which is how we break ties
        data = [point for point in data]
        self.tree = DT_builder(
            data,
            [i for i in range(len(data[0]) - 1)],
            mode(map(class_attr, data))
        )

    def classify(self, p):
        return self.tree.classify(p)

    def classify_many(self, *points):
        return map(self.tree.classify, points)

    def __str__(self):
        return strfy_node(self.tree)

def DT_builder(data, attr, default):
    '''construct a subtree node from data
    data must be sorted by class
    attr is the list of attributes that can be split
    '''
    if not data:
        return LeafNode(default)

    class_attr = itemgetter(-1)
    data = sorted(data, reverse=1, key=class_attr)
    # if all data have the same class
    if class_attr(data[0]) == class_attr(data[-1]):
        return LeafNode(class_attr(data[0]))

    data_mode = mode(map(class_attr, data))
    if not attr:
        return LeafNode(data_mode)
        
    # choose attribute based on max information gain
    best = min(attr, key=lambda at: split_entropy(itemgetter(at), data))
    attr.remove(best)
    subtree = InnerNode(best, data_mode)
    best = itemgetter(best)
    data.sort(key=best)
    for key, subgroup in groupby(data, best):
        subtree.children[key] = DT_builder(subgroup, list(attr), data_mode)
    return subtree



if __name__ == '__main__':
    from argparse import ArgumentParser
    from csv import reader
    arg = ArgumentParser()
    arg.add_argument('datafile', type=open, help='CSV file containing data to build the decision tree')
    print(DecisionTree(reader(arg.parse_args().datafile)))
