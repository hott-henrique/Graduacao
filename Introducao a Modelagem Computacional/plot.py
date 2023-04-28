import argparse

from io import StringIO

import numpy as np
import matplotlib.pyplot as plt


def read_pipe_as_string_io() -> StringIO:
    content = list()

    while True:
        try:
            content.append(input())
        except:
            break;

    return StringIO('\n'.join(content))

def load_simulation(file_path: str = '') -> tuple[np.ndarray, np.ndarray]:
    file = file_path if file_path else read_pipe_as_string_io()

    data = np.loadtxt(file, delimiter=',').T

    steps = data[0]
    simulation = data[[ i for i in range(1, data.shape[0]) ]]

    return steps, simulation

def plot(simulation_data: tuple[np.ndarray, np.ndarray], output_file: str, **kwargs):
    steps, simulation = simulation_data
    fig, ax = plt.subplots()

    fig.set_size_inches(8, 6)

    ax.grid()

    ax.set(
        title=kwargs.pop("title", None),
        xlabel=kwargs.pop("xlabel", None),
        ylabel=kwargs.pop("ylabel", None),
    )

    labels = kwargs.pop("labels", list())

    columns = kwargs.pop("columns")
    if not columns:
        columns = [ i for i in range(len(simulation)) ]

    for i in columns:
        ax.plot(steps, simulation[i], label=labels[i] if labels else None)

    if labels:
        fig.legend()

    fig.savefig(output_file)

def main(**kwargs):
    plot(
        simulation_data=load_simulation(kwargs.pop("csv_file")),
        output_file=kwargs.pop("output_file"),
        **kwargs if kwargs else dict()
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--csv-file",
        type=str,
        required=False,
        default='',
        help="File to read csv. " \
             "If not specified, read from stding untill EOF."
    )

    parser.add_argument("--output-file", type=str, required=True)

    parser.add_argument(
        "--title",
        type=str,
        required=False
    )

    parser.add_argument(
        "--xlabel",
        type=str,
        required=False
    )

    parser.add_argument(
        "--ylabel",
        type=str,
        required=False
    )

    parser.add_argument("--labels",
        type=str,
        nargs="*",
        required=False,
        help="Label for each line in plot. " \
             "If specified, it must have one element for each column in file, " \
             "even if not ploting all columns."
    )

    parser.add_argument(
        "--columns",
        type=int,
        nargs="*",
        required=False,
        default=list(),
        help="Plot only specified columns."
    )

    args = parser.parse_args()

    main(
        csv_file=args.csv_file,
        output_file=args.output_file,
        title=args.title,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
        labels=args.labels,
        columns=args.columns,
    )

