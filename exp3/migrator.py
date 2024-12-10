import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time

from variables import *


class MetaModel:
    def __init__(self, country_code, timestamps=[], co2_emissions=[], start=None, end=None):
        self.country_code = country_code
        try:
            self.timestamps = timestamps.tolist()
        except:
            self.timestamps = timestamps

        try:
            self.co2_emissions = co2_emissions.tolist()
        except:
            self.co2_emissions = co2_emissions

        if (start is not None) and (end is not None):
            self.trim_metamodels_by_time(start, end)

        self.total_emissions = sum(self.co2_emissions)
        self.total_emissions = self.total_emissions / 1e3 # emissions in tons   , at marconi scale
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

    metamodel = MetaModel(timestamps=metamodels[0].timestamps, co2_emissions=co2_emissions, country_code="EU")

    return migration_count, metamodel


def align_metamodels_by_size(metamodels):
    shortest = len(metamodels[0].timestamps)

    for metamodel in metamodels:
        if len(metamodel.timestamps) < shortest:
            shortest = len(metamodel.timestamps)

    for metamodel in metamodels:
        metamodel.timestamps = metamodel.timestamps[:shortest]
        metamodel.co2_emissions = metamodel.co2_emissions[:shortest]

    return metamodels


def output_analysis():
    for metamodel in metamodels:
        # print all the relevant details on one line with new line at the end
        print(f"{metamodel.country_code} ----- {metamodel.total_emissions}")

    print("Granularity 15 leads to total emissions of ",
          migrate_at_granularity(metamodels, granularity=15)[1].total_emissions, "kg with",
          migrate_at_granularity(metamodels, granularity=15)[0], "migrations")
    print("Granularity 60 leads to total emissions of ",
          migrate_at_granularity(metamodels, granularity=60)[1].total_emissions, "kg with",
          migrate_at_granularity(metamodels, granularity=60)[0], "migrations")
    print("Granularity 240 leads to total emissions of ",
          migrate_at_granularity(metamodels, granularity=240)[1].total_emissions, "kg with",
          migrate_at_granularity(metamodels, granularity=240)[0], "migrations")
    print("Granularity 1440 leads to total emissions of ",
          migrate_at_granularity(metamodels, granularity=1440)[1].total_emissions, "kg with",
          migrate_at_granularity(metamodels, granularity=1440)[0], "migrations")

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
