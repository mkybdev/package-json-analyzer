import argparse

from .preprocessing.load import load
from .preprocessing.preprocess import preprocess
from .common.export_df import export_df


def main():

    parser = argparse.ArgumentParser(description="Analyze package.json files.")
    parser.add_argument(
        "dir",
        type=str,
        help="Directory containing package.json files OR name of dumped dataset",
    )
    parser.add_argument("--sample", type=int, help="Number of samples to analyze")
    parser.add_argument("--dump", type=str, help="Name of the dataset to dump")
    args = parser.parse_args()

    rawData = load(args.dir, args.sample, args.dump)
    data = preprocess(rawData)
    export_df(data)


if __name__ == "__main__":
    main()
