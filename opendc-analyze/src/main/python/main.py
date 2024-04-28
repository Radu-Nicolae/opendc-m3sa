import os
import sys
import time

import matplotlib.pyplot as plt

import utils
from models.MultiModel import MultiModel


def main():
    # change directory to the main project directory
    # sleep for 3 seconds


    print("current pathn is: ", os.getcwd())
    os.chdir(utils.SIMULATION_FOLDER_PATH)

    power_draw_multimodel = MultiModel("carbon_emission")
    power_draw_multimodel.generate()


main()

# arg that worked "outoutput/toppology-experiment"



# python main is run from /Users/raz/atlarge/opendc/opendc-analyze/src/main/python
# kotline runs from
