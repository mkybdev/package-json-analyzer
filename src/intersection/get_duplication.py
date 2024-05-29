import pandas as pd


def get_duplication(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    target = df[["name"] + cols].dropna()
    res = []
    for _, row in target.iterrows():
        if all(map(lambda x: isinstance(row[x], dict), cols)):
            common_keys = set(row[cols[0]].keys())
            for col in cols:
                if col == cols[0]:
                    continue
                common_keys = common_keys.intersection(set(row[col].keys()))
            if common_keys:
                res.append({"name": row["name"], "duplication": list(common_keys)})
    return pd.DataFrame(res)
