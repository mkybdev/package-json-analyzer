from ..common.logger import *
import pandas as pd


def get_probability(series: pd.Series) -> pd.DataFrame:
    if all(isinstance(item, type(series[0])) for item in series) and all(
        isinstance(item, list) for item in series
    ):
        # リストの全要素をフラットにする
        all_keywords = [item for sublist in series for item in sublist]

        # フラットにしたリストをSeriesに変換
        flat_keywords = pd.Series(all_keywords)

        # 各要素の出現回数をカウント
        value_counts = flat_keywords.value_counts()

        # 全要素数を取得
        total_count = len(series)

        # 各要素の出現確率を計算
        probabilities = value_counts / total_count
        keywords_prob = pd.DataFrame(probabilities).rename(
            columns={"count": "probability"}
        )
        return keywords_prob
    else:
        error(
            "Series must contain only one type of data, and each element must be a list."
        )
        return pd.DataFrame()
