import os
from os import sys

from input_parser import read_input
from models.MetaModel import MetaModel
from models.MultiModel import MultiModel
from accuracy_evaluator import accuracy_evaluator
import pandas as pd


def main():
    multimodel = MultiModel(user_input=read_input(sys.argv[2]),path=sys.argv[1])
    multimodel.generate_plot()

    metamodel = MetaModel(multimodel)
    metamodel.output()


if __name__ == "__main__":
    main()
