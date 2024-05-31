import pandas as pd
from sklearn.decomposition import PCA  # type: ignore
import matplotlib.pyplot as plt

from package_json_analyzer.clustering.get_pca_loadings import get_loadings
from package_json_analyzer.common.export_image import export_image  # type: ignore


def pca(X: pd.DataFrame, X_tfidf: pd.DataFrame, kmeans: pd.DataFrame):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_tfidf)
    fig = plt.figure()
    plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=kmeans.labels_,
        cmap="viridis",
        marker="o",
        edgecolor="k",
        s=50,
        alpha=0.6,
    )
    plt.colorbar()
    plt.title("PCA - Cluster Visualization")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid()
    export_image(fig, "PCA", "clustering/kmeans/pca", quiet=True)
    get_loadings(X_tfidf, X)
