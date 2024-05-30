import pandas as pd
from tqdm import tqdm  # type: ignore

from .vectorize import vectorize
from ..common.logger import *
from ..common.format_df import format_df
from ..common.export_df import export_df
from .kmeans import kmeans as km


class Clustering:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        if not set(cols).issubset(df.columns):
            error(f"All columns: {cols} must be in the input data.")
        self.df = format_df(df, cols, index="name")
        self.cols = cols
        self.X = self.df[cols]
        self.X_tfidf = vectorize(self.X)
        self.y = self.df["name"]

    def kmeans(self) -> list[pd.DataFrame]:
        return km(self.X, self.X_tfidf, self.y)

    def run(self):
        kmeans_list = self.kmeans()
        for i, kmeans_df in tqdm(
            enumerate(kmeans_list), desc="RUNNING CLUSTERING ANALYSIS"
        ):
            export_df(kmeans_df, "clustering/kmeans", str(i), quiet=True)
