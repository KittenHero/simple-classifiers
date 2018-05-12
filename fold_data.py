from argparse import ArgumentParser
from csv import reader
from os.path import splitext
from itertools import filterfalse, tee, cycle, chain
from contextlib import redirect_stdout

def command_line_args():
    clargs = ArgumentParser()
    clargs.add_argument('infile', type=open, help='data to be folded')
    clargs.add_argument('--outfile', '-o', help='destination file')
    clargs.add_argument('--nfold', '-n', type=int, default=10, help='number of folds')
    clargs = clargs.parse_args()
    if clargs.outfile is None:
        clargs.outfile = splitext(clargs.infile.name)[0] + '-folds.csv'
    return clargs

def partition(pred, iterable):
   'Use a predicate to partition entries into false entries and true entries' 
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def partition_by_class(data):
    return partition(lambda row: row[-1] == 'no', data)

def stratifold(nfold, *classes):
    'create nfold folds with data stratified by classes'
    folds = [[] for _ in range(nfold)]
    # deals out data to each fold in a circle
    for data, fold in zip(chain.from_iterable(classes), cycle(folds)):
        fold.append(data)
    return folds

if __name__ == '__main__':
    args = command_line_args()

    folds = stratifold(args.nfold, *partition_by_class( reader(args.infile) ))

    with open(args.outfile, 'w') as out:
        with redirect_stdout(out):

            for n, fold in enumerate(folds, start=1):
                print(f'fold{n}')
                print('\n'.join(','.join(row) for row in fold), end='\n\n')
