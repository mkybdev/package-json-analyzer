import pandas as pd
from sklearn.manifold import TSNE  # type: ignore
import matplotlib.pyplot as plt

from package_json_analyzer.clustering.get_pca_loadings import get_loadings
from package_json_analyzer.common.export_image import export_image


def tsne(X: pd.DataFrame, X_tfidf: pd.DataFrame, kmeans: pd.DataFrame):
    tsne = TSNE(
        n_components=2, random_state=42, perplexity=min(30, X_tfidf.shape[0] - 1)
    )
    X_tsne = tsne.fit_transform(X_tfidf)
    fig = plt.figure()
    plt.scatter(
        X_tsne[:, 0],
        X_tsne[:, 1],
        c=kmeans.labels_,
        cmap="viridis",
        marker="o",
        edgecolor="k",
        s=50,
        alpha=0.6,
    )
    plt.colorbar()
    plt.title("t-SNE - Cluster Visualization")
    plt.xlabel("t-SNE Feature 1")
    plt.ylabel("t-SNE Feature 2")
    plt.grid()
    export_image(fig, "t-SNE", "clustering/kmeans/tsne", quiet=True)
