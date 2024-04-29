import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import utils
from .Model import Model


class MultiModel:
    def __init__(self, input_metric, window_size=10):
        # the following metrics are set in the latter functions
        self.measure_unit = None
        self.metric = None
        self.raw_models = None
        self.output_folder = None
        self.computed_data = []
        self.input_folder = utils.RAW_OUTPUT_FOLDER_PATH
        self.window_size = window_size

        self.check_and_return_metric(input_metric)
        self.set_output_folder()
        self.init_models()
        self.compute()

    def set_output_folder(self):
        if self.metric == "power_draw":
            self.output_folder = utils.ENERGY_ANALYSIS_FOLDER_PATH
            # create a new file called analysis.txt
            with open(utils.SIMULATION_ANALYSIS_FOLDER_NAME + "/" + utils.ENERGY_ANALYSIS_FOLDER_NAME + "/analysis.txt",
                      "a") as f:
                f.write("")
        elif self.metric == "carbon_emission":
            self.output_folder = utils.EMISSIONS_ANALYSIS_FOLDER_PATH
            with open(
                utils.SIMULATION_ANALYSIS_FOLDER_NAME + "/" + utils.EMISSIONS_ANALYSIS_FOLDER_NAME + "/analysis.txt",
                "a") as f:
                f.write("")

        else:
            raise ValueError("Invalid metric. Please choose from 'power_draw', 'emissions'")

    def init_models(self):
        # os.chdir("./raw-output")
        models = []

        folder_prefix = "./raw-output"

        for simulation_folder in os.listdir(folder_prefix):
            output_folder = f"{folder_prefix}/{simulation_folder}/seed=0"
            models.append(Model(
                host=pd.read_parquet(output_folder + "/host.parquet"),
                server=pd.read_parquet(output_folder + "/server.parquet"),
                service=pd.read_parquet(output_folder + "/service.parquet")
            ))

        self.raw_models = models



    def check_and_return_metric(self, input_metric):
        if input_metric not in ["power_draw", "carbon_emission"]:
            raise ValueError("Invalid metric. Please choose from 'power_draw', 'carbon_emission'")
        self.metric = input_metric
        self.measure_unit = "W" if self.metric == "power_draw" else "gCO2"

    def mean_of_chunks(self, series):
        return series.groupby(np.arange(len(series)) // self.window_size).mean(numeric_only=True)

    def get_windowed_averages(self, metric, aggreagtion_function=np.mean):
        for model in self.raw_models:
            self.computed_data.append(
                self.mean_of_chunks(
                    model.host
                )
            )

    def generate(self):
        self.compute()
        self.setup_plot()
        self.plot_windowed_average()
        self.save_plot()

    def save_plot(self):
        os.chdir("./" + utils.SIMULATION_ANALYSIS_FOLDER_NAME + "/" + self.metric + "/")
        plt.savefig("multimodel_metric=" + self.metric + "_window_size=" + str(self.window_size) + ".png")
        os.chdir('../../')  # return to the original directory

    def setup_plot(self):
        plt.figure(figsize=(30, 10))
        plt.title(self.metric)
        plt.xlabel("Time [s]")
        plt.ylim(0, 400)
        plt.ylabel(self.metric + " [W]")
        plt.grid()

    def plot_windowed_average(self, metric):
        data = self.get_windowed_averages(metric)
        for model in self.computed_data:
            plt.plot(model)
