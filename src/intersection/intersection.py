from .get_duplication import get_duplication
from .get_frequency import get_frequency


class Intersection:
    def __init__(self, df, cols):
        self.df = df
        self.cols = cols
        self.duplication = get_duplication(df, cols)
        self.frequency = get_frequency(df, get_duplication(df, cols), cols)
