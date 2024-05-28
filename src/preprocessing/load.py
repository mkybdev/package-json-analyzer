import os
import pickle
import random
import json
from appdirs import user_cache_dir

from .load_dump import load_dump
from ..common.logger import *
from ..common import constants


def load(root_dir, sample, dump):

    loaded_data = []

    if os.path.exists(root_dir):

        for dirpath, _, filenames in os.walk(root_dir):

            if "package.json" in filenames:
                package_json_path = os.path.join(dirpath, "package.json")
                with open(package_json_path, "r", encoding="utf-8") as f:
                    try:
                        package_data = json.load(f)
                        loaded_data.append(package_data)
                    except json.JSONDecodeError as e:
                        error(f"Error decoding JSON from {package_json_path}: {e}")

        if dump is None:
            info("Loaded data, but dump name not provided. Continuing without dumping.")

        else:
            cache_dir = os.path.join(
                user_cache_dir("package-json-analyzer", "pja"), dump
            )
            os.makedirs(cache_dir, exist_ok=True)
            constants.DUMP_PATH = cache_dir

            cache_file_path = os.path.join(cache_dir, "data.pkl")

            with open(cache_file_path, "wb") as cache_file:
                pickle.dump(loaded_data, cache_file)
                info("Loaded data and saved to cache.")

    else:
        loaded_data = load_dump(root_dir)
        if loaded_data is None:
            error("No such directory or dumped dataset.")

    if sample is None:
        return loaded_data
    else:
        if sample > len(loaded_data):
            error("Sample size exceeds the number of loaded packages.")
        return random.sample(loaded_data, sample)
