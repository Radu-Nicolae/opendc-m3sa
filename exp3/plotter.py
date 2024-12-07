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


def plot_all_emissions(metamodels, start, end, plot_title):
    plt.figure(figsize=(20, 10))

    i = 0
    for metamodel in metamodels:
        timestamps = pd.to_datetime(metamodel.timestamps)
        plt.plot(timestamps, metamodel.co2_emissions, label=metamodel.country_code, color=colorblind_friendly_colors[i],
                 width=5, linestyle=linestyles[i % len(linestyles)])
        i += 1

    padding = pd.Timedelta(days=1)  # Adjust as needed
    plt.xlim(start - padding, end + padding)

    # Define x-ticks
    num_ticks = 4  # Adjust as needed
    x_ticks_positions = pd.date_range(start, end, periods=num_ticks)
    x_ticks_labels = [date.strftime('%d/%m') for date in x_ticks_positions]  # Labels without the year
    plt.xticks(ticks=x_ticks_positions, labels=x_ticks_labels, fontsize=38)  # Bigger font size

    # Set y-axis range
    min_co2, max_co2 = -30, 500  # Specify your minimum and maximum y-values here
    plt.ylim(min_co2, max_co2)

    y_ticks = [0, 100, 200, 300, 400]
    plt.yticks(fontsize=38, ticks=y_ticks)  # Bigger font size
    plt.ylabel("CO2 Emission (gCO2/h)", fontsize=38)
    plt.xlabel("Time (day/month)", fontsize=38)
    plt.grid(True)

    # Adjust plot margins  # Adjust the left and right padding here
    # the legend will be on two rows, and many columns
    # thickness of the lines is 5
    plt.legend(loc='upper center', fancybox=True, shadow=True, ncol=10, fontsize=58, bbox_to_anchor=(0.5, 1.15))
    plt.savefig(plot_title)
    plt.show()
