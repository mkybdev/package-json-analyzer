from ..common.logger import *
from collections import Counter
import pandas as pd
from tqdm import tqdm # type: ignore


def get_frequency(
    df: pd.DataFrame, duplication: pd.DataFrame, cols: list[str]
) -> pd.DataFrame:

    all_elements = [
        element for sublist in duplication["duplication"] for element in sublist
    ]

    # 出現頻度をカウント
    frequency_counter = Counter(all_elements)

    # Counterオブジェクトをデータフレームに変換
    frequency_df = pd.DataFrame(
        frequency_counter.items(), columns=["Element", "Frequency"]
    ).sort_values(by="Frequency", ascending=False)

    elements_to_check = frequency_df["Element"].tolist()

    for i, series in tqdm(
        enumerate([df[col].dropna() for col in cols]),
        desc="INTERSECTION: CALCULATING FREQUENCY",
        leave=False,
    ):
        # 各要素がdictのキーとして出現する回数をカウント
        key_counts = {element: 0 for element in elements_to_check}
        for d in series:
            if isinstance(d, dict):
                for element in elements_to_check:
                    if element in d.keys():
                        key_counts[element] += 1
            # key_countsをfrequency_dfに追加
            frequency_df[f"Dict_Key_Count_{cols[i]}"] = frequency_df["Element"].map(
                key_counts
            )

    return frequency_df
