"""
A model is the output of simulator. It contains the data the simulator output, under a certain topology, seed,
workload, datacenter configuration, etc. A model is further used in the analyzer as part of the MultiModel class,
and further in the MetaModel class.

:param sim: the simulation data of the model
"""
import json
from dataclasses import dataclass, field

class Model:
    """
    Represents a single simulation output containing various data metrics collected under specific simulation conditions.
    A Model object stores raw and processed simulation data and is designed to interact with higher-level structures like
    MultiModel and MetaModel for complex data analysis.
    """

    def __init__(self, path, raw_sim_data, id):
        self.path = path
        self.raw_sim_data = raw_sim_data
        self.id = id
        self.processed_sim_data = []
        self.cumulative_time_series_values = []
        self.cumulated = 0.0
        self.experiment_name = ""
        self.margins_of_error = []
        self.topologies = []
        self.workloads = []
        self.allocation_policies = []
        self.carbon_trace_paths = []

    def parse_trackr(self):
        """
        Parses the 'trackr.json' file located in the model's base path to extract and store detailed experimental metadata.
        This method enhances the model with comprehensive contextual information about the simulation environment.
        """
        trackr_path = self.path + "/trackr.json"
        try:
            with open(trackr_path) as f:
                trackr = json.load(f)
                model_data = trackr.get(self.id, {})
                self.experiment_name = model_data.get('name', "")
                self.topologies = model_data.get('topologies', [])
                self.workloads = model_data.get('workloads', [])
                self.allocation_policies = model_data.get('allocationPolicies', [])
                self.carbon_trace_paths = model_data.get('carbonTracePaths', [])
        except FileNotFoundError:
            print(f"File not found: {trackr_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {trackr_path}")



