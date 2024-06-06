from unittest import skip
import networkx as nx  # type: ignore
from tqdm import tqdm  # type: ignore
import matplotlib.pyplot as plt

from package_json_analyzer.common.export_image import export_image

from ..common.logger import *


def make_network(flatten_conditional_probabilities):

    skipped_list_empty = []
    skipped_list_failed = []

    keys = flatten_conditional_probabilities.keys()

    for key in tqdm(keys, desc="MAKING COOCCURRENCE NETWORK"):
        if flatten_conditional_probabilities[key].empty:
            skipped_list_empty.append(key)
            continue
        try:
            # ネットワーク図の描画
            fig = plt.figure()
            G = nx.DiGraph()

            # ノードとエッジを追加
            for _, row in flatten_conditional_probabilities[key].head(200).iterrows():
                G.add_edge(row["Base"], row["Target"], weight=row["Probability"])

            # ノードのサイズを調整するための辞書を作成
            node_sizes = {
                node: sum([d["weight"] for _, _, d in G.edges(node, data=True)]) * 3000
                for node in G.nodes()
            }

            # エッジの幅を調整するためのリストを作成
            edge_widths = [d["weight"] * 10 for _, _, d in G.edges(data=True)]

            # ポジションを設定
            pos = nx.spring_layout(G, k=0.15, iterations=20)

            nx.draw(
                G,
                pos,
                with_labels=True,
                node_size=[node_sizes[node] for node in G.nodes()],
                width=edge_widths,
                edge_color="blue",
                node_color="lightblue",
                font_size=18,
                font_weight="normal",
            )
            plt.title(key)
            export_image(fig, key, "cooccurrence/network", quiet=True)
        except:
            skipped_list_failed.append(key)
            continue

    if skipped_list_empty:
        info(f"Combinations {skipped_list_empty} was skipped: Empty data.")
    if skipped_list_failed:
        info(f"Combinations {skipped_list_failed} was skipped: Failed to make network.")
