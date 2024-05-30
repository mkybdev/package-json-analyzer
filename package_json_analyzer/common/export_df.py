import os
import pandas as pd

from . import constants
from .logger import *


def export_df(df: pd.DataFrame, dir: str, name: str):
    dir_path = os.path.join(constants.OUTPUT_PATH, dir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, name + ".csv")

    with open(file_path, "w") as file:
        df.to_csv(file, index=False)
        info(f"Exported output: {file_path}")
