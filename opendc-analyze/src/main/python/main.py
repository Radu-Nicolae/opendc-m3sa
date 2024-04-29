import os
import time

import experiments
import utils
from models.MultiModel import MultiModel


def main():
    os.chdir(utils.SIMULATION_FOLDER_PATH)
    experiments.exp1_window_sizes(
        window_sizes=[5,50,500,5000]
    )


main()
