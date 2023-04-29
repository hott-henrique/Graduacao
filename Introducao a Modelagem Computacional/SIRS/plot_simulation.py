import argparse
from io import StringIO
import os

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

def plot(
        simulation_data: tuple[np.ndarray, np.ndarray],
        output_file: str,
        experimental_data: np.ndarray,
        y0: np.ndarray
    ):
    steps, simulation = simulation_data

    N = np.sum(y0)

    R = N - (experimental_data[:, 1] + experimental_data[:, 2])

    experimental_data = np.hstack((experimental_data, R[np.newaxis].T))

    fig, axes = plt.subplots(nrows=1, ncols=3)

    fig.set_size_inches(16, 8)

    fig.suptitle("SIRS")

    labels = [ 'S', 'I', 'R' ]

    for i in range(1, 4):
        ax = axes[i - 1]

        ax.grid()

        ax.set(
            xlabel="Time (Days)",
            ylabel="Amount",
        )

        ax.set_ylabel(f"[ {labels[i - 1]} ]")

        ax.plot(steps, simulation[i - 1], color=(0/255, 0/255, 255/255))
        ax.plot(experimental_data[:, 0], experimental_data[:, i], 'd', label="Experimental Data", color=(1.0, 0.0, 0.0))

        xticks = np.arange(start=0, stop=len(experimental_data), step=1)
        yticks = np.arange(start=0, stop=N + 100, step=100)

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        ax.set_xlim(0, np.max(xticks))
        ax.set_ylim(0, np.max(yticks))

        ax.legend()

    fig.savefig(output_file)

def main(output_file, experimental_data, y0, csv_file: str = ''):
    plot(
        simulation_data=load_simulation(csv_file),
        output_file=output_file,
        experimental_data=experimental_data,
        y0=y0
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--experimental-data", type=str, required=True)
    parser.add_argument("--y0", type=np.float64, nargs="+", required=True)
    parser.add_argument("--input-file", type=str, default='')
    parser.add_argument("--output-file", type=str, required=True)

    args = parser.parse_args()

    dirs = os.path.dirname(args.output_file)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    main(
        csv_file=args.input_file,
        output_file=args.output_file,
        experimental_data=np.loadtxt(args.experimental_data, delimiter=','),
        y0=np.array(args.y0)
    )

