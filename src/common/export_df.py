import os

from . import constants
from .logger import *


def export_df(df):
    file_path = os.path.join(constants.DUMP_PATH, "out.csv")

    with open(file_path, "w") as file:
        df.to_csv(file, index=False)
        info("Exported output.")
