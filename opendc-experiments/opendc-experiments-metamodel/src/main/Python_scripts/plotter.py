import matplotlib.pyplot as plt
import pandas as pd

class DataPlotter:
    def __init__(self, dfs):
        self.dfs = dfs  # now dfs is expected to be a list of DataFrames

    def plot_cpu_usage(self):
        self._plot_metric('cpu_usage', 'CPU usage (%)')

    def plot_power_total(self):
        self._plot_metric('power_total', 'Power Total (W)')

    def plot_cpu_limit(self):
        self._plot_metric('cpu_limit', 'CPU Limit (%)')

    def plot_cpu_demand(self):
        self._plot_metric('cpu_demand', 'CPU Demand (%)')

    def plot_cpu_utilization(self):
        self._plot_metric('cpu_utilization', 'CPU Utilization (%)')

    def plot_cpu_time_active(self):
        self._plot_metric('cpu_time_active', 'CPU Time Active (s)')

    def plot_cpu_time_idle(self):
        self._plot_metric('cpu_time_idle', 'CPU Time Idle (s)')

    def plot_cpu_time_steal(self):
        self._plot_metric('cpu_time_steal', 'CPU Time Steal (s)')

    def plot_cpu_time_lost(self):
        self._plot_metric('cpu_time_lost', 'CPU Time Lost (s)')

    def plot_servers_active(self):
        self._plot_metric('servers_active', 'Servers Active')

    def plot_attempts_success(self):
        self._plot_metric('attempts_success', 'Attempts Success')

    def plot_mem_capacity(self):
        self._plot_metric('mem_capacity', 'Memory Capacity')

    def plot_cpu_count(self):
        self._plot_metric('cpu_count', 'CPU Count')

    def plot_cpu_limit(self):
        self._plot_metric('cpu_limit', 'CPU Limit (%)')

    def plot_guests_running(self):
        self._plot_metric('guests_running', 'Guests Running')

    def plot_guests_terminated(self):
        self._plot_metric('guests_terminated', 'Guests Terminated')

    def plot_guests_error(self):
        self._plot_metric('guests_error', 'Guests Error')

    def plot_guests_invalid(self):
        self._plot_metric('guests_invalid', 'Guests Invalid')


    def plot_attempts_failure(self):
        self._plot_metric('attempts_failure', 'Attempts Failure')

    def plot_attempts_error(self):
        self._plot_metric('attempts_error', 'Attempts Error')

    def plot_hosts_up(self):
        self._plot_metric('hosts_up', 'Hosts Up')

    def plot_hosts_down(self):
        self._plot_metric('hosts_down', 'Hosts Down')

    def plot_servers_pending(self):
        self._plot_metric('servers_pending', 'Servers Pending')


    def _plot_metric(self, metric_name, y_label):
        metric_values = []
        for df in self.dfs:  # iterate over the list of DataFrames
            if metric_name in df.columns:
                metric_values.append(df[metric_name])
            else:
                print(f"DataFrame does not have '{metric_name}' column")
                metric_values.append(pd.Series([None]))  # Handle missing data

        plt.figure(figsize=(20, 10))
        for metric_value in metric_values:
            plt.plot(metric_value)
        plt.xlabel('Time (s)')
        plt.ylabel(y_label)
        plt.title(f'{y_label} for each model')
        plt.show()
