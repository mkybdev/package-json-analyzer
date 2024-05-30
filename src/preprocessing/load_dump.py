import os
import pickle
from appdirs import user_cache_dir

from ..common.logger import *
from ..common import constants


def load_dump(name: str):

    cache_dir = os.path.join(user_cache_dir("package_json_analyzer", "pja"), name)
    constants.DUMP_PATH = cache_dir
    cache_file_path = os.path.join(cache_dir, "data.pkl")

    if os.path.exists(cache_file_path):
        with open(cache_file_path, "rb") as cache_file:
            loaded_data = pickle.load(cache_file)
            info("Loaded data from cache.")
        return loaded_data
    else:
        return None
