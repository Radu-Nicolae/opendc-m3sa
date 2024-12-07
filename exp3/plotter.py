import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from migrator import *

def plotter(metamodels):
    color = "gray"
    plt.figure(figsize=(30, 10))
    for metamodel in metamodels:
        # if the country code contains eu
        if metamodel.country_code[:2] == "EU":
            color = "red"
        else:
            color = "lightgray"
        plt.plot(metamodel.timestamps, metamodel.co2_emissions, label=metamodel.country_code, color=color)

    plt.xlabel("Timestamp")
    plt.ylabel("CO2 Emissions")
    plt.legend()
    plt.show()
