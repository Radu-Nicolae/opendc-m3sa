import subprocess
import sys
from pathlib import Path
import os
import matplotlib.pyplot as plt


def main():
    # give as program argument word "hello world"
    path_to_script = Path(__file__).resolve().parent.parent.parent / "./opendc-analyze/src/main/python/main.py"
    path_to_outputs = "reproducibility-capsule-scripts/scripts-data/figure17/outputs"
    path_to_setup_fig_a = "reproducibility-capsule-scripts/scripts-data/figure17/inputs/m3sa-setup-window-1.json"
    path_to_setup_fig_b = "reproducibility-capsule-scripts/scripts-data/figure17/inputs/m3sa-setup-window-10.json"
    path_to_setup_fig_c = "reproducibility-capsule-scripts/scripts-data/figure17/inputs/m3sa-setup-window-100.json"
    path_to_setup_fig_d = "reproducibility-capsule-scripts/scripts-data/figure17/inputs/m3sa-setup-window-1000.json"

    # Use these paths in your script as needed
    os.system(f"python3 {path_to_script} {path_to_outputs} {path_to_setup_fig_a}")
    os.system(f"python3 {path_to_script} {path_to_outputs} {path_to_setup_fig_b}")
    os.system(f"python3 {path_to_script} {path_to_outputs} {path_to_setup_fig_c}")
    os.system(f"python3 {path_to_script} {path_to_outputs} {path_to_setup_fig_d}")

    # move the figures into the experiments-output folder
    os.system(
        f"docker cp m3sa-experiments-container:opendc/reproducibility-capsule-scripts/scripts-data/figure17/outputs/simulation-analysis/power-draw ./experiments-outputs/figures/figure17/")


if __name__ == '__main__':
    """
    Figure 17 is composed of four subplots, which we will call 17a, 17b, 17c, and 17d. Figure 17 represents the visual
    difference between window sizes of 1, 10, 100, and 1,000.
    """
    main()
    # call main function of m3sa, the firle is situated in opendc/opendc-analyze/src/main/python/main.py
