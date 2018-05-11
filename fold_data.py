from argparse import ArgumentParser
from csv import reader, writer

def command_line_args():
    clargs = ArgumentParser()
    clargs.add_argument('infile', type=open, help='data to be folded')
    clargs.add_argument('--outfile', '-o', help='destination file')
    return clargs.parse_args()

cl = command_line_args()
