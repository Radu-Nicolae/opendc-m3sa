import numpy as np
import pandas as pd
import os
from migrator import *
from plotter import *
from variables import *

def co2_traces(path):
    metamodels = []
    for file in os.listdir(path):
        if file.endswith('.parquet') and "EU" not in file:
            metamodels.append(
                MetaModel(
                    country_code = file[:2],
                    co2_emissions = pd.read_parquet(path + file)["carbon_emission"].values
                )
            )

    for metamodel in metamodels:
        metamodel.timestamps = np.arange(1, len(metamodel.co2_emissions) + 1)


    return metamodels


def get_lowest_at_timestamp(metamodels, timestamp_index):
    min_emission = metamodels[0].co2_emissions[timestamp_index]
    location = metamodels[0].country_code

    for metamodel in metamodels:
        if metamodel.co2_emissions[timestamp_index] < min_emission:
            min_emission = metamodel.co2_emissions[timestamp_index]
            location = metamodel.country_code

    for metamodel in metamodels:
        if metamodel.country_code == location:
            return metamodel

    raise Exception("No metamodel with country code " + location + " found.")


def migrate(metamodels, granularity=1, country_code="EU"):
    model_len = len(metamodels[0].timestamps)
    migration_count = 0

    current_model = get_lowest_at_timestamp(metamodels, 0)
    co2_emissions = []

    i = 0
    while i < model_len:
        if i % granularity == 0:
            lowest_model = get_lowest_at_timestamp(metamodels, i)
            if current_model.country_code.lower() != lowest_model.country_code.lower():
                migration_count += 1
                current_model = lowest_model

        co2_emissions.append(current_model.co2_emissions[i])
        i += 1

    metamodel = MetaModel(
        timestamps=metamodels[0].timestamps,
        co2_emissions=co2_emissions,
        country_code=country_code
    )
    print("Migration done. There are a total of " + str(migration_count) + " migrations.")
    return migration_count, metamodel

def save_model_to_file(metamodels, migrated, path):
    # create a new parquet file which contains two columns: one is the timestamp and the other is the carbon_intensity.
    # the timestamps are the same as in a "inputs/co2/AT-2023-06.parquet"

    timestamps = pd.read_parquet("inputs/co2/AT-2023-06.parquet")["timestamp"].values
    min_entries = min(len(timestamps), len(migrated.co2_emissions))
    df = pd.DataFrame({
        "timestamp": timestamps[:min_entries],
        "carbon_emission": migrated.co2_emissions[:min_entries]
    })

    df.to_parquet(path)


if __name__ == '__main__':
    metamodels = co2_traces("metamodels/")
    metamodels = align_metamodels_by_size(metamodels)
    for metamodel in metamodels:
        print(metamodel.country_code, metamodel.total_emissions)

