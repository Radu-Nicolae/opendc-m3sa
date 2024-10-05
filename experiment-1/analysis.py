# %%

import pandas as pd
# %%

df_host = pd.read_parquet("output/surfsara/raw-output/0/seed=0/host.parquet")
df_service = pd.read_parquet("output/surfsara/raw-output/0/seed=0/service.parquet")
df_task = pd.read_parquet("output/surfsara/raw-output/0/seed=0/task.parquet")

df_carbon = pd.read_parquet("carbonTraces/carbon_2022_new.parquet")
df_validation = pd.read_parquet("validation/surfsara.parquet")

# %%

df_host.groupby("timestamp").carbon_emission.aggregate("sum").plot()

# %%

df_host.carbon_intensity