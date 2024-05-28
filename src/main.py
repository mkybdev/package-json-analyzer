from .preprocessing.load import *
from .preprocessing.preprocess import *
# from .intersection import test as intersection
# from .cooccurrence import test as cooccurrence
# from .clustering import test as clustering
import argparse

def main():

    parser = argparse.ArgumentParser(description='Analyze package.json files.')
    parser.add_argument('dir', type=str, help='Directory containing package.json files OR name of dumped dataset')
    parser.add_argument('--sample', type=int, help='Number of samples to analyze')
    parser.add_argument('--dump', type=str, help='Name of the dataset to dump')
    args = parser.parse_args()

    data = load(args.dir, args.sample, args.dump)
    print(len(preprocess(data)))

if __name__ == '__main__':
    main()