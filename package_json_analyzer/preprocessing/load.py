import os
import pickle
import random
import json
from tqdm import tqdm  # type: ignore
import yaml  # type: ignore
import yamlcore  # type: ignore
from appdirs import user_cache_dir  # type: ignore

from .load_dump import load_dump
from ..common.logger import *
from ..common import constants


def load(
    root_dir: str,
    sample: int = -1,
    name: str = "",
    out_dir: str = os.path.join(os.path.expanduser("~"), "Downloads"),
) -> list[dict]:

    loaded_data: list[dict] = []
    skipped_files = []

    if os.path.exists(root_dir):

        for dirpath, _, filenames in tqdm(os.walk(root_dir), desc="LOADING DATA"):

            if "package.json" in filenames:
                package_json_path = os.path.join(dirpath, "package.json")
                with open(package_json_path, "r", encoding="utf-8") as f:
                    try:
                        package_data = json.load(f)
                        loaded_data.append(package_data)
                    except:
                        skipped_files.append(package_json_path)
            elif any(filename.endswith(".yml") for filename in filenames):
                for filename in filenames:
                    if filename.endswith(".yml"):
                        yml_path = os.path.join(dirpath, filename)
                        with open(yml_path, "r", encoding="utf-8") as f:
                            try:
                                yml_data = yaml.load(f, Loader=yamlcore.CoreLoader)
                                loaded_data.append(yml_data)
                            except:
                                skipped_files.append(yml_path)

        if skipped_files:
            info(f"Skipped loading {len(skipped_files)} files: {skipped_files}")

        if name == "":
            info("Loaded data, but dump name not provided. Continuing without dumping.")

        else:
            cache_dir = os.path.join(
                user_cache_dir("package_json_analyzer", "pja"), name
            )
            os.makedirs(cache_dir, exist_ok=True)
            constants.DUMP_PATH = cache_dir

            cache_file_path = os.path.join(cache_dir, "data.pkl")

            with open(cache_file_path, "wb") as cache_file:
                pickle.dump(loaded_data, cache_file)
                info("Loaded data and saved to cache.")

    else:
        loaded_data = load_dump(root_dir)
        if loaded_data == []:
            error("No such directory or dumped dataset.")
        else:
            try:
                os.rmdir(constants.OUTPUT_PATH)
            except:
                pass
            constants.OUTPUT_PATH = os.path.join(out_dir, root_dir)

    if sample < 0:
        info(f"Loaded {len(loaded_data)} packages.")
        return loaded_data
    else:
        if sample > len(loaded_data):
            error("Sample size exceeds the number of loaded packages.")
        constants.IS_SAMPLED = True
        info(f"Sampling {sample} packages from {len(loaded_data)} loaded packages.")
        return random.sample(loaded_data, sample)
