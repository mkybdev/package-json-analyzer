from .clustering import Clustering
from .cooccurrence import Cooccurrence
from .intersection import Intersection
from .statistics import Statistics


def run_all(data, intersection_list=None, cooccurrence_list=None, clustering_list=None):
    statistics = Statistics(data)
    statistics.run()

    if intersection_list:
        intersection = Intersection(data, intersection_list)
        intersection.run()

    if cooccurrence_list:
        cooccurrence = Cooccurrence(data, cooccurrence_list)
        cooccurrence.run()

    if clustering_list:
        clustering = Clustering(data, clustering_list)
        clustering.run()
