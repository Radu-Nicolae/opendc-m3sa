import os
import matplotlib.pyplot as plt

from models.MultiModel import MultiModel


def main():
    # os.chdir('../../demo/output/')  # change directory to the main project directory

    # create a white image, called red.png, and save it in the current folder
    print("I reached some line")

    plt.figure(figsize=(10, 10))
    plt.plot([1, 2, 3, 4])
    plt.savefig("reddd.png")
    plt.show()


    # multimodel = MultiModel()
    # multimodel.plot()


main()
