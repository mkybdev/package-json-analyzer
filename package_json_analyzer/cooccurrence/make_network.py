import networkx as nx  # type: ignore
from tqdm import tqdm  # type: ignore
import matplotlib.pyplot as plt
import os

from ..common import constants
from ..common.logger import *


def make_network(flatten_conditional_probabilities):
    keys = flatten_conditional_probabilities.keys()

    for key in tqdm(keys, desc="MAKING COOCCURRENCE NETWORK"):
        if flatten_conditional_probabilities[key].empty:
            info(f"{key}: Empty data. Skipping...")
            continue
        try:
            # ネットワーク図の描画
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

            dir_path = os.path.join(constants.OUTPUT_PATH, "cooccurrence/network")
            os.makedirs(dir_path, exist_ok=True)
            file_path = os.path.join(dir_path, key + ".png")
            plt.savefig(file_path)
            plt.close()
        except:
            info(f"Failed to make network of {key}. Skipping...")
