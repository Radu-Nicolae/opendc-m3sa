import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

MS_GRANULARITY = 300000
SCALE_TO_MARCONI = 2982 / 150  # we simulate just 150 nodes, but we have 3812 nodes in the real network

DAY = MS_GRANULARITY * 12 * 24
HOUR = MS_GRANULARITY * 12
MINUTE_5 = MS_GRANULARITY

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

# make an array with all existent line styles in python
linestyles = ['-', '--', '-.', ':']

# make an array with all existent markers in python
markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']


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
        # if filename[:2] == "at" or filename[:2] == "fr":
        #     continue
        if filename.endswith(".parquet"):
            file = pd.read_parquet(path + filename).groupby('timestamp').sum()
            timestamps = file.index
            co2_emissions = file["carbon_intensity"]
            metamodels.append(
                MetaModel(
                    country_code=filename[:2],  # country code is (must be) the first 2 characters of the file name
                    timestamps=timestamps,
                    co2_emissions=co2_emissions
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
    migration_model = []
    location_of_running = select_model_by_location(metamodels, starting_location)

    i = 0

    while i < model_length:
        # calculate the migration cost
        if i % (migration_granularity / MS_GRANULARITY) == 0:
            if location_of_running != select_model_by_location(metamodels, starting_location):  # if we need to migrate
                location_of_running = select_model_by_location(metamodels, starting_location)
                migration_count += 1

        migration_model.append(location_of_running.co2_emissions[i])
        i += 1

    migration_model_total = round(sum(migration_model) * SCALE_TO_MARCONI / 1e6, 2)
    return migration_count, migration_model_total, migration_model

def count_migrations_per_month(metamodels, migration_granularity, starting_location):
    migration_counts = []
    for month in range(1, 13):
        migration_count, _, _ = simulate_with_migration(metamodels, migration_granularity, starting_location)
        migration_counts.append(migration_count)
    return migration_counts



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


if __name__ == '__main__':
    metamodels = get_metamodels("./inputs/co2/")

    # plot_total_emissions(metamodels)
    print("Country, Tons CO2")
    for metamodel in metamodels:
        # print all the relevant details on one line with new line at the end
        print(f"{metamodel.country_code} ----- {metamodel.total_emissions}")

    starts = [pd.Timestamp('2023-01-01 00:00:00'), pd.Timestamp('2023-02-01 00:00:00'),
              pd.Timestamp('2023-03-01 00:00:00'), pd.Timestamp('2023-04-01 00:00:00'),
              pd.Timestamp('2023-05-01 00:00:00'), pd.Timestamp('2023-06-01 00:00:00'),
              pd.Timestamp('2023-07-01 00:00:00'), pd.Timestamp('2023-08-01 00:00:00'),
              pd.Timestamp('2023-09-01 00:00:00'), pd.Timestamp('2023-10-01 00:00:00'),
              pd.Timestamp('2023-11-01 00:00:00'), pd.Timestamp('2023-12-01 00:00:00')]

    ends = [pd.Timestamp('2023-01-31 00:00:00'), pd.Timestamp('2023-02-28 00:00:00'),
            pd.Timestamp('2023-03-31 00:00:00'), pd.Timestamp('2023-04-30 00:00:00'),
            pd.Timestamp('2023-05-31 00:00:00'), pd.Timestamp('2023-06-30 00:00:00'),
            pd.Timestamp('2023-07-31 00:00:00'), pd.Timestamp('2023-08-31 00:00:00'),
            pd.Timestamp('2023-09-30 00:00:00'), pd.Timestamp('2023-10-31 00:00:00'),
            pd.Timestamp('2023-11-30 00:00:00'), pd.Timestamp('2023-12-31 00:00:00')]

    plot_names = ["jan2023.pdf", "feb2023.pdf", "mar2023.pdf", "apr2023.pdf", "may2023.pdf", "jun2023.pdf",
                  "jul2023.pdf", "aug2023.pdf", "sep2023.pdf", "oct2023.pdf", "nov2023.pdf", "dec2023.pdf"]

    # plot_all_emissions(metamodels, starts[0], ends[0], "legend.pdf")

    # print(count_migrations_per_month(metamodels, 300000, "it"))


    # for i in range(0, 12):
    #     plot_all_emissions(metamodels=metamodels, start=starts[i], end=ends[i], plot_title=plot_names[i])
