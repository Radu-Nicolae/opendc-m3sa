from sys import argv
from models import MultiModel, MetaModel
from util import SimulationConfig, read_input


def parse_input() -> tuple[SimulationConfig, str]:
    if len(argv) != 3:
        print(
            f"Invalid input.\n"
            f"Usage: {argv[0]} <config.json> <path/>"
        )
        exit(1)

    return read_input(argv[2]), argv[1]


def main() -> None:
    simulation_config, path = parse_input()

    multi_model: MultiModel = MultiModel(*parse_input())
    multi_model.generate_plot()

    if simulation_config.is_metamodel:
        meta_model: MetaModel = MetaModel(multi_model)


if __name__ == "__main__":
    main()
