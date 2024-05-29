from .get_duplication import get_duplication
from .get_frequency import get_frequency

import pandas as pd


class Intersection:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        self.df = df
        self.cols = cols
        self.dup = None

    def duplication(self):
        self.dup = get_duplication(self.df, self.cols)
        return self.dup

    def frequency(self):
        return get_frequency(
            self.df,
            get_duplication(self.df, self.cols) if self.dup is None else self.dup,
            self.cols,
        )
