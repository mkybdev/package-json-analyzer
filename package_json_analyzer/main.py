import argparse
import os

from package_json_analyzer.clustering.clustering import Clustering

from .preprocessing.load import load
from .preprocessing.preprocess import preprocess
from .common.export_df import export_df
from .common.logger import *
from .common import constants
from .intersection.intersection import Intersection
from .cooccurrence.cooccurrence import Cooccurrence


def main():

    parser = argparse.ArgumentParser(description="Analyze package.json files.")
    parser.add_argument(
        "target",
        type=str,
        help="Path to the directory containing package.json files / Name of dumped dataset",
    )
    parser.add_argument("-s", "--sample", type=int, help="Number of samples to analyze")
    parser.add_argument(
        "-n", "--name", type=str, help="Name of the dataset to be dumped"
    )
    parser.add_argument(
        "-o",
        "--out",
        type=str,
        default=os.path.join(os.path.expanduser("~"), "Downloads"),
        help="Output directory",
    )
    args = parser.parse_args()

    if os.path.exists(args.out):
        if args.name is None:
            constants.OUTPUT_PATH = os.path.join(args.out, "pja_output")
        else:
            constants.OUTPUT_PATH = os.path.join(args.out, args.name)
        os.makedirs(constants.OUTPUT_PATH, exist_ok=True)
    else:
        error("Output directory does not exist.")

    rawData = load(args.target, args.sample, args.name, args.out)
    data = preprocess(rawData)

    intersection = Intersection(data, ["dependencies", "devDependencies"])
    export_df(intersection.duplication(), "intersection", "duplication")
    export_df(intersection.frequency(), "intersection", "frequency")

    cooccurrence = Cooccurrence(
        data, ["license", "keywords", "files", "dependencies", "devDependencies"]
    )
    export_df(
        cooccurrence.conditional_probability(),
        "cooccurrence",
        "conditional_probability",
    )

    clustering = Clustering(
        data, ["scripts", "devDependencies", "dependencies", "keywords"]
    )
    export_df(clustering.kmeans(), "clustering", "kmeans")


if __name__ == "__main__":
    main()
