from sklearn.decomposition import PCA  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore

import numpy as np
import pandas as pd
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt

from package_json_analyzer.common.export_image import export_image


def get_loadings(X_tfidf: pd.DataFrame, X: pd.DataFrame):
    # データの標準化
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(X_tfidf)

    target = PCA(n_components=2)  # 2つの主成分を取得
    principalComponents = target.fit_transform(data_scaled)
    loadings = target.components_.T * np.sqrt(target.explained_variance_)

    # 主成分の負荷量とデータフレームを作成
    loadings_df = pd.DataFrame(loadings, columns=["PC1", "PC2"], index=X_tfidf.columns)

    # # サンプリング（データセットが大きい場合のため）
    # sample_size = 500  # サンプルサイズを適宜調整
    # indices = np.random.choice(principalComponents.shape[0], sample_size, replace=False)
    # sampled_data = principalComponents[indices]

    # 負荷量が0.5以上の要素のみを抽出
    filtered_loadings_df = loadings_df[
        (abs(loadings_df["PC1"]) > 0.5) | (abs(loadings_df["PC2"]) > 0.5)
    ]

    for value_to_search in filtered_loadings_df.copy().index:
        # 特定の値を含む行を抽出する関数
        def contains_value(row, value):
            columns_with_value = []
            for col in row.index:
                if isinstance(row[col], list) and value in row[col]:
                    columns_with_value.append(col)
            return columns_with_value

    # データフレーム全体を検索して行と含まれていたカラムを抽出します
    results = X.apply(lambda row: contains_value(row, value_to_search), axis=1)
    matching_rows = X[results.apply(len) > 0]
    columns_with_value = results[results.apply(len) > 0]

    if len(matching_rows) == 0:
        filtered_loadings_df = filtered_loadings_df.rename(
            index={value_to_search: f"{value_to_search} (?)"}
        )
    else:
        filtered_loadings_df = filtered_loadings_df.rename(
            index={
                value_to_search: f"{value_to_search} ({set([columns_with_value[matching_rows.index[i]][0] for i in range(len(matching_rows.index))])})"
            }
        )

    # ヒートマップの作成
    fig = plt.figure()
    sns.heatmap(filtered_loadings_df, annot=False, cmap="coolwarm", fmt=".2f")
    plt.title(f"Heatmap of PCA Loadings (with |PC1| and |PC2| > 0.5)")
    plt.xlabel("Principal Components")
    plt.ylabel("Variables")
    plt.tight_layout()
    export_image(
        fig,
        f"PCA Loadings",
        f"clustering/kmeans/pca",
        quiet=True,
    )
