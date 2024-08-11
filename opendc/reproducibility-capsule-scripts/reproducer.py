"""
This script is the main entry point for the reproducibility. It will receive arguments from the command line, which would either run all the figures and tables, or a specific one.

Possible arguments:
- help: show the help message
- all: run all the figures and tables
- figure x: run the figure x, where x can be {17, 18, 19, 20, 21, 27, 28, 31, 33, 34, 35, 36, 37}
- table y: run the table y, where y can be {1, 2, 3, 4, 5, 6}

Example:
    ```python3 reproducer.py help```
    ```python3 reproducer.py all```
    ```python3 reproducer.py figure 33```
    ```python3 reproducer.py table 4```
"""

import sys
import os
import subprocess
import time

FIGURE_IDS = [17, 18, 19, 20, 21, 27, 28, 31, 33, 34, 35, 36, 37]
TABLE_IDS = [1, 2, 3, 4, 5, 6]


def print_help():
    print(__doc__)


def run_all():
    for figure_id in FIGURE_IDS:
        run_figure(figure_id)

    for table_id in TABLE_IDS:
        run_table(table_id)


def run_figure(figure_id):
    """
    Run the figure with the given id. The figure will be generated and saved in the figures folder.
    :param figure_id: int, the id of the figure to run (possible values are: {17, 18, 19, 20, 21, 27, 28, 31, 33, 34, 35, 36, 37})
    :return: print "Completed figure {figure_id}"
    """
    print(f"Running figure {figure_id}...", end='', flush=True)  # Flush the output immediately
    time.sleep(0.5)  # Sleep to simulate the figure processing time
    subprocess.run(["python3", f"scripts-figures/figure{figure_id}.py"])
    print(f"\rCompleted figure {figure_id}       ", flush=True)


def run_table(table_id):
    print("Running table", table_id)


def main():
    if len(sys.argv) == 1:
        print_help()
        return

    if sys.argv[1] == "help":
        print_help()
        return

    if sys.argv[1] == "all":
        run_all()
        return

    if sys.argv[1] == "figure":
        if len(sys.argv) != 3:
            print("Invalid number of arguments.")
            return
        figure_id = int(sys.argv[2])
        if figure_id not in FIGURE_IDS:
            print("Invalid figure id. Possible values are:", FIGURE_IDS)
            return
        run_figure(figure_id)
        return

    if sys.argv[1] == "table":
        if len(sys.argv) != 3:
            print("Invalid number of arguments.")
            return
        table_id = int(sys.argv[2])
        if table_id not in TABLE_IDS:
            print("Invalid table id. Possible values are:", TABLE_IDS)
            return
        run_table(table_id)
        return


if __name__ == "__main__":
    main()
