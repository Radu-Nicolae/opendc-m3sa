import numpy as np
import pandas as pd
import os
from migrator import *
from plotter import *

SCALE_TO_MARCONI = 2982 / 150

def co2_traces(path):
    metamodels = []
    for file in os.listdir(path):
        # if the file ends in parquet and doesn't have EU in the name
        if file.endswith('.parquet') and "EU" not in file:
            metamodels.append(
                MetaModel(
                    country_code = file[:2],
                    co2_emissions = pd.read_parquet(path + file)["carbon_intensity"].values
                )
            )

    for metamodel in metamodels:
        # add the timestamps such that each metamodel has as many timestamps as values in carbon intenstity.
        # the timestamps start from 1 and go as  1, 2, 3, 4 ...
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
        "carbon_intensity": migrated.co2_emissions[:min_entries]
    })

    df.to_parquet(path)


if __name__ == '__main__':
    metamodels = co2_traces("inputs/co2/")
    metamodels = align_metamodels_by_size(metamodels)
    migration_15min = migrate(metamodels, granularity=1, country_code="EU-15min")[1]
    save_model_to_file(metamodels, migration_15min, path="inputs/EU-migration=15min-2023-06.parquet")

    migration_1h = migrate(metamodels, granularity=4, country_code="EU-1h")[1]
    migration_4h = migrate(metamodels, granularity=16, country_code="EU-4h")[1]
    migration_8h = migrate(metamodels, granularity=32, country_code="EU-8h")[1]
    migration_1d = migrate(metamodels, granularity=96, country_code="EU-1d")[1]
    save_model_to_file(
        metamodels,
        ,
        path="inputs/EU-migration=1d-2023-06.parquet"
    )

    metamodels.append(migration_15min)
    metamodels.append(migration_1h)
    metamodels.append(migration_4h)
    metamodels.append(migration_8h)
    metamodels.append(migration_1d)

    for metamodel in metamodels:


    plotter(metamodels)
    # plotter(metamodels)

