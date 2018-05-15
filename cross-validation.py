from fold_data import stratifold, partition_by_class
from csv import reader
import subprocess
import os


if __name__ == '__main__':
    expected = subprocess.check_output(['cut', '-d,', '-f9', 'pima.csv'], encoding='ascii').split('\n')
    testfile = 'test.csv'
    with open(testfile, 'w') as f:
        print(subprocess.check_output(['cut', '-d,', '-f1-8', 'pima.csv'], encoding='ascii'), end='', file=f)
    output = subprocess.check_output(['python', 'MyClassifier.py', 'pima.csv', testfile , 'NB'], encoding='ascii').split('\n')
    os.remove(testfile)
    print('NB accuracy on whole set', sum(e == o for e, o in zip(expected, output)) / len(expected))
