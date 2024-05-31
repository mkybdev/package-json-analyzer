from sklearn.cluster import KMeans  # type: ignore
import pandas as pd
from collections import Counter

from package_json_analyzer.clustering.get_pca_loadings import get_loadings
from package_json_analyzer.clustering.pca import pca  # type: ignore
from package_json_analyzer.clustering.tsne import tsne  # type: ignore

from ..common.logger import *


def kmeans(
    X: pd.DataFrame, X_tfidf: pd.DataFrame, y: pd.Series, num_clusters: int = 5
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    columns = X.columns.values
    # KMeansを用いたクラスタリング
    try:
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X_tfidf)
    except:
        error("An error occurred while running KMeans. Maybe the dataset is too small.")

    pca(X, X_tfidf, kmeans)
    tsne(X, X_tfidf, kmeans)

    res = []

    # クラスタラベルを元のデータフレームXに追加
    X["cluster"] = kmeans.labels_
    X.insert(0, "name", y)

    # クラスタごとにデータをグループ化
    for cluster_num in range(num_clusters):
        cluster_data = X[X["cluster"] == cluster_num]
        cluster_feature: dict[str, list] = dict()
        for column in columns:
            # すべてのリストを一つのリストに結合し、出現頻度をカウント
            all_items = []
            for items in cluster_data[column]:
                if isinstance(items, list):  # カラムのデータがリスト型であることを確認
                    all_items += items
                else:
                    all_items += []  # リスト型でない場合は空のリストを追加
            item_counts = Counter(all_items)
            # 出現回数が多い上位5項目を取得（適宜調整可能）
            top_items = item_counts.most_common(5)
            cluster_feature[column] = top_items
        rows = []
        for key, values in cluster_feature.items():
            for value in values:
                rows.append([value[0], key, value[1]])
        rows.sort(key=lambda x: x[2], reverse=True)
        res.append(
            (cluster_data, pd.DataFrame(rows, columns=["item", "field", "count"]))
        )

    return res
