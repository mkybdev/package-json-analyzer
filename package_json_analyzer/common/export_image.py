import matplotlib.pyplot as plt
import os

from ..common import constants
from ..common.logger import *


def export_image(fig: plt.Figure, name: str, dir: str, quiet: bool = False):
    dir_path = os.path.join(constants.OUTPUT_PATH, dir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, name + ".png")
    fig.savefig(file_path)
    plt.close()
    if not quiet:
        info(f"Exported output: {file_path}")
