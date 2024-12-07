import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time

from exp3.co2_migrator import SCALE_TO_MARCONI

# recorded data
#       | MIGRATION COUNT PER INTERVAL|
# Month  15min  60min  240min  1440min
# Jan    4      4        4      2
# Feb    24     24       20     2
# Mar    73     73       33     3
# Apr    43     43       25     7
# May    17     17       6      0
# Jun    112    112      69     11
# Jul    105    105      46     7
# Aug    112    112      58     8
# Sep    30     30       21     0
# Oct    112    111      53     8
# Nov    62     62       28     6
# Dec    53     53       16     3

# Granularity 15 leads to total emissions of 59.43 kg with 112 migrations
# Granularity 60 leads to total emissions of 59.43 kg with 112 migrations
# Granularity 240 leads to total emissions of 137.3 kg with 69 migrations
# Granularity 1440 leads to total emissions of 124.22 kg with 11 migrations

# experiment results
# FR ----- 189.01
# CH ----- 67.35
# RO ----- 6654.41
# ES ----- 3075.23
# PT ----- 679.89
# AT ----- 537.28
# DE ----- 11419.32
# IT ----- 1274.66
# DK ----- 1407.52
# BA ----- 6026.98
# LU ----- 3365.57
# MK ----- 7242.4
# SK ----- 615.13
# HU ----- 5404.42
# BE ----- 608.74py
# HR ----- 1316.96
# SE ----- 81.73
# LV ----- 453.57
# GR ----- 1634.75
# CZ ----- 2980.95
# NO ----- 85.8
# SI ----- 2474.47
# FI ----- 617.16
# BG ----- 2049.83
# NL ----- 3504.91
# PL ----- 6124.35
# LT ----- 851.8
# RS ----- 5144.83
# EE ----- 2666.25
# Granularity 15 leads to total emissions of 59.43 kg with 112 migrations
# Granularity 60 leads to total emissions of 59.43 kg with 112 migrations
# Granularity 240 leads to total emissions of 137.3 kg with 69 migrations
# Granularity 1440 leads to total emissions of 124.22 kg with 11 migrations


colorblind_friendly_colors = [
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermilion
    "#CC79A7",  # reddish purple

    "#F0A3FF",  # bright purple
    "#0075DC",  # cerulean
    "#993F00",  # burnt orange
    "#4C005C",  # dark purple
    "#191919",  # grey
    "#005C31",  # dark green
    "#2BCE48",  # green
    "#FFCC99",  # peach
    "#808080",  # gray
    "#94FFB5",  # mint
    "#8F7C00",  # mustard
    "#9DCC00",  # lime
    "#C20088",  # magenta

    "#003380",  # navy blue
    "#FFA405",  # tangerine
    "#FFA8BB",  # pink
    "#426600",  # olive
    "#FF0010",  # red orange
    "#5EF1F2",  # bright cyan
    "#00998F",  # teal
    "#E0FF66",  # light lime
    "#740AFF",  # violet
    "#990000",  # dark red

    "#FFFF80",  # light yellow
    "#FF5005",  # bright orange
    "#FFFF00",  # yellow
    "#FFFFFF",  # white
    "#000000",  # black
    "#FFB200",  # vivid orange
    "#ABCDEF",  # pale blue
    "#FA58F4",  # hot pink
    "#00FFCC",  # turquoise
    "#D7DF01",  # yellowish green

    "#8A4117",  # sienna
    "#5CB3FF",  # sky blue
    "#B0E57C",  # tea green
    "#F5E216",  # golden yellow
    "#7851A9",  # royal purple
    "#4A9586",  # blue green
    "#FF0028",  # scarlet
    "#E55B3C",  # terra cotta
    "#C6DC67",  # pistachio
]
SCALE_TO_MARCONI = 2982 / 150

linestyles = ['-', '--', '-.', ':']
markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']


class MetaModel:
    def __init__(self, country_code, timestamps=[], co2_emissions=[], start=None, end=None):
        self.country_code = country_code
        try:
            self.timestamps = timestamps.tolist()
        except:
            self.timestamps = timestamps
        self.timestamps_minutes = []

        try:
            self.co2_emissions = co2_emissions.tolist()
        except:
            self.co2_emissions = co2_emissions

        if (start is not None) and (end is not None):
            self.trim_metamodels_by_time(start, end)

        self.total_emissions = sum(self.co2_emissions)
        self.total_emissions = self.total_emissions# emissions in tons   , at marconi scale
        self.total_emissions = round(self.total_emissions, 2)


    def trim_metamodels_by_time(self, start, end):
        """
        :param start: pd.Timestamp object
        :param end: pd.Timestamp object
        :return: n/a, just updated in metamodel self object
        """

        index_of_start = 0
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())

        for i in range(len(self.timestamps)):
            if time.mktime(self.timestamps[i].timetuple()) >= start:
                index_of_start = i
                break

        index_of_termination = 0
        for i in range(len(self.timestamps)):
            if time.mktime(self.timestamps[i].timetuple()) >= end:
                index_of_termination = i
                break

        self.timestamps = self.timestamps[index_of_start:index_of_termination]
        self.timestamps_minutes = self.timestamps_minutes[index_of_start:index_of_termination]
        self.co2_emissions = self.co2_emissions[index_of_start:index_of_termination]




def get_metamodels(path):
    metamodels = []
    for filename in os.listdir(path):
        if filename.endswith(".parquet"):
            file = pd.read_parquet(path + filename)
            timestamps = file.index
            co2 = file["carbon_emission"]
            metamodels.append(
                MetaModel(
                    country_code=filename[:2],  # country code is (must be) the first 2 characters of the file name
                    timestamps=timestamps,
                    co2_emissions=co2
                )
            )

    return metamodels


def select_model_by_location(metamodels, location):
    for metamodel in metamodels:
        if metamodel.country_code.lower() == location.lower():
            return metamodel

    raise Exception(f"Location {location} not found in metamodels")


def minimum_at_timestamp(metamodels, timestamp):
    """
    :param metamodels:
    :param timestamp: the timestamp, in miliseconds. e.g., 300000 means 300 seconds
    :return:
    """
    # index must be integer
    index = int(timestamp / MS_GRANULARITY)
    min = metamodels[0].co2_emissions[index]
    location = metamodels[0].country_code
    for metamodel in metamodels:
        if metamodel.co2_emissions[index] < min:
            min = metamodel.co2_emissions[index]
            location = metamodel.country_code

    return min, location


def plot_total_emissions(metamodels):
    # plot a data distribution, per country, as a boxplot
    data = []
    for metamodel in metamodels:
        data.append(metamodel.total_emissions)

    plt.figure(figsize=(5, 5))
    plt.boxplot(data, vert=False)
    plt.xlabel("Total CO2 emissions (tons)")
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


def get_lowest_emission_location_at_timestamp(metamodels, timestamp_index):
    min_emission = metamodels[0].co2_emissions[timestamp_index]
    location = metamodels[0].country_code

    for metamodel in metamodels:
        if metamodel.co2_emissions[timestamp_index] < min_emission:
            min_emission = metamodel.co2_emissions[timestamp_index]
            location = metamodel.country_code

    for metamodel in metamodels:
        if metamodel.country_code.lower() == location.lower():
            return metamodel

    raise Exception(f"Location {location} not found in metamodels")


def migrate_at_granularity(metamodels, granularity):
    """
    Granularity is in multiples of 15 minutes. for instance, if the granularity is 15, then choose 15. If it is 1h, then 4.
    :param metamodels:
    :param granularity:
    :param starting_location:
    :return:
    """
    granularity /= 15
    model_len = len(metamodels[0].timestamps)
    migration_count = 0

    current_model = get_lowest_emission_location_at_timestamp(metamodels, 0)
    co2_emissions = []

    i = 0
    while i < model_len:
        if i % granularity == 0:
            lowest_model = get_lowest_emission_location_at_timestamp(metamodels, i)
            if current_model.country_code.lower() != lowest_model.country_code.lower():
                migration_count += 1
                current_model = lowest_model

        co2_emissions.append(current_model.co2_emissions[i])

        i += 1

    metamodel = MetaModel(
        timestamps=metamodels[0].timestamps,
        co2_emissions=co2_emissions,
        country_code="EU"
    )

    return migration_count, metamodel


def align_metamodels_by_size(metamodels):
    shortest = len(metamodels[0].timestamps)

    for metamodel in metamodels:
        if len(metamodel.timestamps) < shortest:
            shortest = len(metamodel.timestamps)

    for metamodel in metamodels:
        metamodel.timestamps = metamodel.timestamps[:shortest]
        metamodel.co2_emissions = metamodel.co2_emissions[:shortest]
        metamodel.timestamps_minutes = metamodel.timestamps_minutes[:shortest]

    return metamodels


def output_analysis():
    for metamodel in metamodels:
        # print all the relevant details on one line with new line at the end
        print(f"{metamodel.country_code} ----- {metamodel.total_emissions}")


    print("Granularity 15 leads to total emissions of ", migrate_at_granularity(metamodels, granularity=15)[1].total_emissions, "kg with", migrate_at_granularity(metamodels, granularity=15)[0], "migrations")
    print("Granularity 60 leads to total emissions of ", migrate_at_granularity(metamodels, granularity=60)[1].total_emissions, "kg with", migrate_at_granularity(metamodels, granularity=60)[0], "migrations")
    print("Granularity 240 leads to total emissions of ", migrate_at_granularity(metamodels, granularity=240)[1].total_emissions, "kg with", migrate_at_granularity(metamodels, granularity=240)[0], "migrations")
    print("Granularity 1440 leads to total emissions of ", migrate_at_granularity(metamodels, granularity=1440)[1].total_emissions, "kg with", migrate_at_granularity(metamodels, granularity=1440)[0], "migrations")

    plt.figure(figsize=(500, 10))
    for metamodel in metamodels:
        plt.plot(metamodel.timestamps, metamodel.co2_emissions, label=metamodel.country_code)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    metamodels = get_metamodels(
        path="metamodels/"
    )
    metamodels = align_metamodels_by_size(metamodels)
    output_analysis()
