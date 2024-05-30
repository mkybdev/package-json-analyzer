import pandas as pd

class Clustering:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        self.df = df
        self.cols = cols
        self.X = self.df[self.cols]
        self.y = self.df["name"]