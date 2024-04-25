import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .Model import Model


class MultiModel:
    def __init__(self):
        models = self.init_models()

    def init_models(self):
        os.chdir('simulation-results/')
        simulation_count = len(os.listdir())
        simulation_folders = os.listdir()
        models = []

        for _ in range(simulation_count):
            os.chdir(simulation_folders[_])
            models.append(Model(
                host=pd.read_parquet("host.parquet"),
                server=pd.read_parquet("server.parquet"),
                service=pd.read_parquet("service.parquet")
            ))
            os.chdir('../')  # return to the original directory

        os.chdir('../')  # return to the original directory
        return models


    def plot(self):
        print("The current path is: ", os.getcwd())


