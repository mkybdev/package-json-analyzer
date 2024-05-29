import pandas as pd


def preprocess(rawData: list[dict]) -> pd.DataFrame:
    all_keys: set = set()
    for entry in rawData:
        all_keys.update(entry.keys())
    data = pd.DataFrame(rawData)
    data = data.reindex(columns=list(all_keys)).dropna(
        thresh=int(len(data) / 100), axis=1
    )
    return data
