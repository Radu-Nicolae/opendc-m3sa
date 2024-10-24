"""
This function is used to parse the seconds to hours, from the list of .parquet files received as parameters.
Hence, if the data is in gCO2/second it will be converted into gCO2/hour.

The parquet file is then changed (overwritten) to reflect the change.
"""

import os
import pandas as pd


def parse_seconds_to_hours(files):
    for file in files:
        df_host = pd.read_parquet(file)

        # Ensure the 'timestamp_absolute' is in datetime format
        df_host['timestamp'] = pd.to_datetime(df_host['timestamp'], unit='ms')

        # Group by hour and sum the emissions
        emissions = df_host.groupby(pd.Grouper(key='timestamp', freq='h'))['carbon_emission'].sum()

        # Convert the series back to a dataframe
        emissions_df = emissions.reset_index()

        # Save the new dataframe back to parquet
        emissions_df.to_parquet(file)
        print(f"File {file} updated with gCO2/hour")


if __name__ == '__main__':
    print("You are at: ", os.getcwd())

    files = [
        "../outputs/raw-output/0/seed=0/host.parquet",
        "../outputs/raw-output/1/seed=0/host.parquet",
        "../outputs/raw-output/2/seed=0/host.parquet",
        "../outputs/raw-output/3/seed=0/host.parquet",
        "../outputs/raw-output/4/seed=0/host.parquet"
    ]

    parse_seconds_to_hours(files)
