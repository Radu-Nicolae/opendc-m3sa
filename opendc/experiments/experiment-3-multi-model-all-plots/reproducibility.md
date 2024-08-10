# Experiment 3 - reproducibility

**Option 1:** Run Scenario CLI, with the following setup.

Main.py code:
```python
from experiments import experiment2
# other imports

def main():
    experiment3.experiment_3()
```

ScenarioCLI arguments:
```
--scenario-path "experiments/experiment-3-multi-model-all-plots/inputs/scenario.json" -p 4 -a
```

ScenarioCLI working directory:
```
/your/path/opendc/
```


**Option 2:** If already have the simulation output files, run only the main.py and skip the simulation time.

Main.py code:
```python
from experiments import experiment2
# other imports

def main():
    experiment3.experiment_3()
```


The output of the experiment is generated in 
```opendc-analyze/src/main/python/analysis.txt```.
