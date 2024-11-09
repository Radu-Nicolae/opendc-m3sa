# Reproducibility for figure 5c

## scenario.json
```json
{
    "name": "outputs/",
    "topologies": [
        {
            "pathToFile": "exp1-fig1/inputs/topologies/topology_linear.json"
        }
    ],
    "workloads": [
        {
            "pathToFile": "exp1-fig1/inputs/surfsara",
            "type": "ComputeWorkload"
        }
    ],
    "carbonTracePaths": [
        "exp1-fig1/inputs/carbon_2022.parquet"
    ],
    "allocationPolicies": [
        {
            "policyType": "Mem"
        }
    ],
    "outputFolder": "exp1-fig1/",
    "runs": 1
}

```


## m3saSetup.json
```shell
{
    "multimodel": true,
    "metamodel": false,
    "metric": "carbon_emission",
    "window_size": 10,
    "window_function": "mean",
    "meta_function": "mean",
    "samples_per_minute": 2,
    "plot_type": "time_series",
    "y_ticks_count": 3,
    "x_ticks_count": 5,
    "y_label": "",
    "y_min": 0,
    "y_max": 6800,
    "current_unit": "gCO2/h",
    "unit_scaling_magnitude": -3,
    "figsize": [15, 6]
}
```


## Multi-Model adjustments
-- divide the results by 7 to match footprinter results
`raw = np.divide(raw, self.unit_scaling) / 7`

## Run M3SA
Arguments for main.py
`"exp1-fig1/outputs" "exp1-fig1/inputs/m3saSetup.json"`

Arguments for M3SACli
`--experiment-path "exp1-fig1/inputs/scenario.json" -m "exp1-fig1/inputs/m3saSetup.json"`

In M3SACli
- take just the first model
