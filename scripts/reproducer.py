"""
This script is the main entry point for the reproducibility. It will receive arguments from the command line, which would
either run all the figures and tables, or a specific one.

Possible arguments (maximum 1):
- all: run all the figures and tables
- figure x: run the figure x, where x can be {17, 18, 19, 20, 21, 27, 28, 31, 33, 34, 35, 36, 37}
- table y: run the table y, where y can be {1, 2, 3, 4, 5, 6}

Example:
    ```python3 reproducer.py figure 33```
    ```python3 reproducer.py table 4```
"""


