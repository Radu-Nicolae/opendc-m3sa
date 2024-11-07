import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.variables import graph_colors
from utils.EnergyData import EnergyData
from datetime import datetime
import pandas as pd

min_power = 40
max_power = 280

def power_model(utilization):
    power_diff = max_power - min_power
    weighted_utilization = utilization**(1/(5))
    
    return (min_power + (power_diff * weighted_utilization)).real

def my_sum(serie):
    idle_power = 1200
    idle_hosts = numHosts - len(serie)
    
    return (idle_hosts * idle_power) + sum(serie)

def add_power_draw(df):
    df["power_draw"] = df["cpu_utilization"].apply(power_model).round(2)


def get_energy_data(start_date, end_date, country_code='NL'):
    start = pd.Timestamp("2022-01-1", tz='Europe/Brussels')
    end = pd.Timestamp("2022-12-31", tz='Europe/Brussels')
    country_code = 'NL'  # Netherlands

    return EnergyData(start, end, country_code)

def plot_graph(df_power, df_emission):
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(10,11), dpi=80)

    title_size = 30
    label_size = 25
    tick_size = 25

    matplotlib.rc('xtick', labelsize=tick_size) 
    matplotlib.rc('ytick', labelsize=tick_size)

    ax1.plot(df_power["power_draw"]/1000, color=graph_colors[0])
    ax1.set_title("Power Draw (kW)", fontsize=title_size)
    # ax1.set_ylim([0,None])
    ax1.grid(axis="both")

    ax2.plot(df_power["energy_mix"], color=graph_colors[0])
    ax2.set_title("Energy Carbon Intensity (gCO2/kWh)", fontsize=title_size)
    ax2.set_ylim([0,None])
    ax2.grid(axis="both")

    ax3.plot(df_emission["carbon_emission"], color=graph_colors[0])
    ax3.set_title("Carbon emission (gCO2/h)", fontsize=title_size)
    ax3.set_xlabel("Time [h]", fontsize=label_size)
    ax3.set_ylim([0,None])
    ax3.grid(axis="both")

    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax3.xaxis.set_minor_locator(mdates.HourLocator())

    props = dict(boxstyle='round', facecolor=graph_colors[-1], alpha=0.5)
    ax1.text(.95, 0.13, "5.A", transform=ax1.transAxes, fontsize=22,
            verticalalignment='center', horizontalalignment='center', bbox=props)
    ax2.text(.95, 0.13, "5.B", transform=ax2.transAxes, fontsize=22,
            verticalalignment='center', horizontalalignment='center', bbox=props)
    ax3.text(.95, 0.13, "5.C", transform=ax3.transAxes, fontsize=22,
            verticalalignment='center', horizontalalignment='center', bbox=props)


    ax3.xaxis.set_major_formatter(
        mdates.DateFormatter("%d/%m"))

    # plt.savefig("figures/footprinter_result.pdf", format="pdf", bbox_inches="tight")

    plt.show()


# %%

def plot_emissions(df_host, start_date, end_date):

    add_power_draw(df_host)
    df_power = df_host.groupby("absolute_timestamp").agg({"power_draw": "sum"})

    energy_data = get_energy_data("2022-01-01", "2022-12-31", "NL")

    res = []
    for timestamp in df_power.index:
        res.append(energy_data.get_energy_mix(timestamp.tz_localize('Europe/Brussels')))
    
    df_power["energy_mix"] = res

    df_power["energy_usage"] = df_power["power_draw"] * 30 / 1000 / 3600

    df_power["carbon_emission"] = df_power["energy_usage"] * df_power["energy_mix"]
    
    
    ##### Aggregate to hours
    df_power_hour = df_power.groupby([df_power.index.day, df_power.index.hour]).agg({"carbon_emission": "sum"})
    df_power_hour["carbon_emission"].to_numpy()

    timestamps = [datetime.strptime(f"2022-10-{day} {hour}", "%Y-%m-%d %H") for day, hour in df_power_hour.index]

    df_emission = pd.DataFrame(df_power_hour["carbon_emission"].to_numpy()[:-1], index = timestamps[:-1], columns=["carbon_emission"])

    plot_graph(df_power, df_emission)