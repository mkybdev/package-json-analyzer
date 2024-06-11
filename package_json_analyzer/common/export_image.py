import os

import constants  # type: ignore
import logger  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def export_image(fig: Figure, name: str, dir: str, quiet: bool = False):
    dir_path = os.path.join(constants.OUTPUT_PATH, dir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, name + ".png")
    fig.savefig(file_path)
    plt.close()
    if not quiet:
        logger.info(f"Exported output: {file_path}")
