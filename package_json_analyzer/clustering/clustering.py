import pandas as pd
from sklearn.cluster import KMeans  # type: ignore
from .vectorize import vectorize
from ..common.format_df import format_df


class Clustering:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        self.df = format_df(df, cols, index="name")
        self.cols = cols
        self.X = self.df[cols]
        self.X_tfidf = vectorize(self.X)
        self.y = self.df["name"]

    def kmeans(self, num_clusters: int = 5) -> pd.DataFrame:
        # KMeansを用いたクラスタリング
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(self.X_tfidf)
        # クラスタリングの結果をyに追加
        res = self.y.to_frame()
        res["cluster"] = kmeans.labels_
        return res
