import os

from src.models.MultiModel import MultiModel


def main():
    os.chdir('../../demo/output/')  # change directory to the main project directory
    multimodel = MultiModel()
    multimodel.plot()


main()
