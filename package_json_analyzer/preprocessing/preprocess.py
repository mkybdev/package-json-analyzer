import pandas as pd


def preprocess(rawData: list[dict]) -> pd.DataFrame:
    print(rawData[:10])
    all_keys: set = set()
    for entry in rawData:
        all_keys.update(entry.keys())
    data = pd.DataFrame(rawData)
    data = data.reindex(columns=list(all_keys))
    return data
