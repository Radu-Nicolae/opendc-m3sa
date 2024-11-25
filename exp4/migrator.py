import pandas as pd
import os
import matplotlib.pyplot as plt

MS_GRANULARITY = 300000
SCALE_TO_MARCONI = 2982 / 150  # we simulate just 150 nodes, but we have 3812 nodes in the real network

DAY = MS_GRANULARITY * 12 * 24
HOUR = MS_GRANULARITY * 12
MINUTE_5 = MS_GRANULARITY


class MetaModel:
    def __init__(self, country_code, timestamps, co2_emissions):
        self.country_code = country_code
        self.timestamps = timestamps.tolist()
        self.co2_emissions = co2_emissions.tolist()
        self.total_emissions = sum(co2_emissions)
        self.total_emissions = self.total_emissions * SCALE_TO_MARCONI / 1e6  # emissions in tons, at marconi scale
        self.total_emissions = round(self.total_emissions, 2)


# class Migrator:
#     def migrate(self):

def get_metamodels(path):
    # for every file at the path, read the file
    metamodels = []
    for filename in os.listdir(path):
        if filename.endswith(".parquet"):
            file = pd.read_parquet(path + filename)
            metamodels.append(
                MetaModel(
                    country_code=filename[:2],  # country code is (must be) the first 2 characters of the file name
                    timestamps=file["timestamp"],
                    co2_emissions=file["carbon_emission"]
                )
            )

    return metamodels

def select_model_by_location(metamodels, location):
    for metamodel in metamodels:
        if metamodel.country_code == location:
            return metamodel

    raise Exception(f"Location {location} not found in metamodels")


def simulate_with_migration(metamodels, migration_granularity, starting_location):
    model_length = len(metamodels[0].timestamps)
    migration_count = 0
    co2_total = []
    location_of_running = select_model_by_location(metamodels, starting_location)

    i = 0
    while i < model_length:
        # calculate the migration cost
        if i % (migration_granularity / MS_GRANULARITY) == 0:
            if location_of_running != select_model_by_location(metamodels, starting_location): # if we need to migrate
                location_of_running = select_model_by_location(metamodels, starting_location)
                migration_count += 1

        co2_total.append(location_of_running.co2_emissions[i])
        i += 1

    return migration_count, sum(co2_total)


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


if __name__ == '__main__':
    metamodels = get_metamodels("./metamodels/")

    # plot_total_emissions(metamodels)
    print("Country, Tons CO2")
    for metamodel in metamodels:
        # print all the relevant details on one line with new line at the end
        print(f"{metamodel.country_code} ----- {metamodel.total_emissions}")

    # minimum co2 emissions as a starting point
    starting_location = minimum_at_timestamp(metamodels=metamodels, timestamp=300000)[1]
    print(
        f"Simulation with migration: {simulate_with_migration(metamodels=metamodels, migration_granularity=DAY, starting_location=starting_location)[1]}.")

    # migrator = Migrator()
    # migrator.migrate()
