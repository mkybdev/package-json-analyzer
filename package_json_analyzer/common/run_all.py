from package_json_analyzer.intersection.intersection import Intersection
from package_json_analyzer.cooccurrence.cooccurrence import Cooccurrence
from package_json_analyzer.clustering.clustering import Clustering


def run_all(data):
    intersection = Intersection(data, ["dependencies", "devDependencies"])
    intersection.run()

    cooccurrence = Cooccurrence(
        data, ["license", "keywords", "files", "dependencies", "devDependencies"]
    )
    cooccurrence.run()

    clustering = Clustering(
        data, ["scripts", "devDependencies", "dependencies", "keywords"]
    )
    clustering.run()
