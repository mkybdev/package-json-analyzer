from sklearn.cluster import KMeans  # type: ignore
import pandas as pd

from ..common.logger import *


def kmeans(X, X_tfidf, y, num_clusters: int = 5) -> list[pd.DataFrame]:
    # KMeansを用いたクラスタリング
    try:
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X_tfidf)
    except:
        error("An error occurred while running KMeans. Maybe the dataset is too small.")

    res = []

    # クラスタラベルを元のデータフレームXに追加
    X["cluster"] = kmeans.labels_
    X.insert(0, "name", y)

    # クラスタごとにデータをグループ化
    for cluster_num in range(num_clusters):
        cluster_data = X[X["cluster"] == cluster_num]
        res.append(cluster_data)

    return res
