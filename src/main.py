from .preprocessing import test as preprocessing
from .intersection import test as intersection
from .cooccurrence import test as cooccurrence
from .clustering import test as clustering

def main():
    preprocessing.test_preprocessing()
    intersection.test_intersection()
    cooccurrence.test_cooccurrence()
    clustering.test_clustering()