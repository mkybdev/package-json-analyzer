import pandas as pd


def preprocess(rawData):
    all_keys = set()
    for entry in rawData:
        all_keys.update(entry.keys())
    data = pd.DataFrame(rawData)
    data = data.reindex(columns=all_keys).dropna(thresh=len(data) / 100, axis=1)
    return data
