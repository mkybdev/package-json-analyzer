import pandas as pd
import os
from tqdm import tqdm # type: ignore
from collections import Counter
from ..common import constants


def get_conditional_probability(
    df: pd.DataFrame, probabilities: dict[str, pd.Series], cols: list[str]
) -> pd.DataFrame:

    cache_dir = os.path.join(constants.DUMP_PATH, "conditional_probabilities")
    os.makedirs(cache_dir, exist_ok=True)
    cached_files = os.listdir(cache_dir)

    conditional_probabilities = pd.DataFrame()

    # 条件付き共起確率を計算する
    probs = {col: probabilities[col] for col in cols}

    # 条件付き共起確率を計算する関数
    def calculate_conditional_probabilities(base_column: str, target_column: str):
        conditional_probs = {}
        total_rows = len(df)

        for base_item in probs[base_column].index:
            base_rows = df[df[base_column].apply(lambda x: base_item in x)]
            base_count = len(base_rows)

            if base_count > 0:
                co_occurrence_counts = Counter(
                    [item for sublist in base_rows[target_column] for item in sublist]
                )
                conditional_probs[base_item] = {
                    k: v / total_rows for k, v in co_occurrence_counts.items()
                }

        return pd.DataFrame(conditional_probs).fillna(0)

    # 各データフレームをフラット化
    def flatten(df: pd.DataFrame, combination: str):
        flat_df = df.unstack().reset_index()
        flat_df.columns = pd.Index(["Base", "Target", "Probability"])
        flat_df.loc[:, ["Combination"]] = combination
        flat_df = flat_df.sort_values(by="Probability", ascending=False)
        return flat_df

    # 各カラムの組み合わせに対して条件付き共起確率を計算
    for base_column in tqdm(
        cols, desc="COOCCURRENCE: CALCULATING CONDITIONAL PROBABILITY", leave=False
    ):
        for target_column in cols:
            if base_column != target_column:
                combination = f"{base_column} -> {target_column}"
                cond_prob_df = pd.DataFrame()
                if not constants.IS_SAMPLED and f"{combination}.csv" in cached_files:
                    cond_prob_df = pd.read_csv(
                        f"{cache_dir}/{combination}.csv",
                        dtype={
                            "Base": str,
                            "Target": str,
                            "Probability": float,
                            "Combination": str,
                        },
                    )
                else:
                    cond_prob_df = flatten(
                        calculate_conditional_probabilities(base_column, target_column),
                        combination,
                    )
                    cond_prob_df.to_csv(f"{cache_dir}/{combination}.csv")
                conditional_probabilities = pd.concat(
                    [conditional_probabilities, cond_prob_df],
                    ignore_index=True,
                )

    return conditional_probabilities
