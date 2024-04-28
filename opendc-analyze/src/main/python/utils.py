import sys

import matplotlib.pyplot as plt

"""
Constants for the main.py file
"""

SIMULATION_FOLDER_PATH = './../../../../demo/' + sys.argv[1]
RAW_OUTPUT_FOLDER_PATH = SIMULATION_FOLDER_PATH + '/raw-output/'
ANALYSIS_FOLDER_PATH = SIMULATION_FOLDER_PATH + '/simulation-analysis/'

EMISSIONS_ANALYSIS_FOLDER_PATH = ANALYSIS_FOLDER_PATH + 'carbon_emission/'
ENERGY_ANALYSIS_FOLDER_PATH = ANALYSIS_FOLDER_PATH + 'power_draw/'

SIMULATION_ANALYSIS_FOLDER_NAME = 'simulation-analysis'
EMISSIONS_ANALYSIS_FOLDER_NAME = 'carbon_emission'
ENERGY_ANALYSIS_FOLDER_NAME = 'power_draw'


"""
Utility functions
"""
def plot_a_figure():
    plt.figure(figsize=(10, 10))
    plt.plot([1, 2, 3, 4])
    plt.savefig("testtt.png")
    plt.show()
