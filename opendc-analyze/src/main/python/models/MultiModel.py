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
        self.models = None
        self.output_folder = None
        self.computed_data = []
        self.input_folder = utils.RAW_OUTPUT_FOLDER_PATH
        self.window_size = window_size
        self.check_and_return_metric(input_metric)
        self.set_output_folder()
        self.init_models()

    def set_output_folder(self):
        if self.metric == "power_draw":
            self.output_folder = utils.ENERGY_ANALYSIS_FOLDER_PATH
        elif self.metric == "carbon_emission":
            self.output_folder = utils.EMISSIONS_ANALYSIS_FOLDER_PATH
        else:
            raise ValueError("Invalid metric. Please choose from 'power_draw', 'emissions'")

    def init_models(self):
        os.chdir("./raw-output")
        simulation_count = len(os.listdir())
        simulation_folders = os.listdir()
        models = []

        for simulation_folder in range(simulation_count):
            simulation_folder_contents = os.listdir(simulation_folders[simulation_folder])
            for i in range(len(simulation_folder_contents)):
                os.chdir(simulation_folders[simulation_folder] + "/seed=" + str(i) + "/")
                models.append(Model(
                    host=pd.read_parquet("host.parquet")[self.metric],
                    server=pd.read_parquet("server.parquet"),
                    service=pd.read_parquet("service.parquet")
                ))
                os.chdir('../../')  # return to the original directory

        os.chdir('../')  # return to the original directory
        self.models = models

    def check_and_return_metric(self, input_metric):
        if input_metric not in ["power_draw", "carbon_emission"]:
            raise ValueError("Invalid metric. Please choose from 'power_draw', 'carbon_emission'")
        self.metric = input_metric
        self.measure_unit = "W" if self.metric == "power_draw" else "gCO2"

    def mean_of_chunks(self, series):
        return series.groupby(np.arange(len(series)) // self.window_size).mean(numeric_only=True)

    def compute(self):
        for model in self.models:
            self.computed_data.append(
                self.mean_of_chunks(
                    model.host
                )
            )

    def generate(self):
        self.compute()
        self.setup_plot()
        self.plot()
        self.save_plot()

    def save_plot(self):
        print("current path is " + os.getcwd())
        newPath = "/" + utils.SIMULATION_ANALYSIS_FOLDER_NAME + "/" + self.metric + "/"
        os.chdir("./" + utils.SIMULATION_ANALYSIS_FOLDER_NAME + "/" + self.metric + "/")
        plt.savefig("newplot.png")

    def setup_plot(self):
        plt.figure(figsize=(30, 10))
        plt.title(self.metric)
        plt.xlabel("Time [s]")
        plt.ylabel(self.metric + " [W]")
        plt.grid()

    def plot(self):
        for model in self.computed_data:
            plt.plot(model)
