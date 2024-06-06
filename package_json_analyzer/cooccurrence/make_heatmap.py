from calendar import c
import re
from tqdm import tqdm  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd
import seaborn as sns  # type: ignore

from package_json_analyzer.common.export_image import export_image
from ..common.logger import *


def convert_format(input_string):
    # 正規表現を使って "X -> Y" 形式を "P(Y | X)" 形式に変換
    pattern = re.compile(r"(\w+)\s*->\s*(\w+)")
    match = pattern.match(input_string)

    if match:
        x = match.group(1)
        y = match.group(2)
        return f"P({y} | {x})"
    else:
        return input_string


def make_heatmap(flatten_conditional_probabilities: dict[str, pd.DataFrame]):

    skipped_list_empty = []
    skipped_list_failed = []

    for key in tqdm(
        flatten_conditional_probabilities.keys(), desc="MAKING COOCCURRENCE HEATMAP"
    ):
        # 結果をピボットテーブルに変換
        pivot_table = (
            flatten_conditional_probabilities[key]
            .head(500)
            .pivot(index="Base", columns="Target", values="Probability")
        )
        if pivot_table.empty:
            skipped_list_empty.append(key)
            continue
        # ヒートマップを描画
        try:
            fig = plt.figure()
            sns.heatmap(pivot_table, annot=False, fmt=".2f", cmap="YlGnBu")
            plt.title(convert_format(key))
            plt.xlabel("Target")
            plt.ylabel("Base")
            plt.tight_layout()
            export_image(fig, key, "cooccurrence/heatmap", quiet=True)
        except:
            skipped_list_failed.append(key)
            continue

    if skipped_list_empty:
        info(f"Combinations {skipped_list_empty} was skipped: Empty data.")
    if skipped_list_failed:
        info(f"Combinations {skipped_list_failed} was skipped: Failed to make heatmap.")
