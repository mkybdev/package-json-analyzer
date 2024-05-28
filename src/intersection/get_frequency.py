from ..common.logger import *
from collections import Counter
import pandas as pd


def get_frequency(df, duplication, cols):

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

    for i, series in enumerate([df[col].dropna() for col in cols]):
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
