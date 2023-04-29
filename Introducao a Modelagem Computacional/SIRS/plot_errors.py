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
    file = file_path if file_path != '' else read_pipe_as_string_io()

    data = np.loadtxt(file, delimiter=',').T

    steps = data[0]
    simulation = data[[ i for i in range(1, data.shape[0]) ]]

    return steps, simulation

def plot(simulation_data: tuple[np.ndarray, np.ndarray], output_file: str):
    steps, simulation = simulation_data

    fig, ax = plt.subplots()

    fig.set_size_inches(8, 6)

    ax.grid()

    ax.set(
        title="Errors over Time",
        xlabel="Time (Days)",
        ylabel="Error",
    )

    for i, y in enumerate(simulation):
        ax.plot(steps, y, color=(255/255, 50/255, 50/255))

    fig.savefig(output_file)

def main(output_file, csv_file: str = ''):
    plot(
        simulation_data=load_simulation(csv_file),
        output_file=output_file,
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str, default='')
    parser.add_argument("--output-file", type=str, required=True)

    args = parser.parse_args()

    dirs = os.path.dirname(args.output_file)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    main(
        csv_file=args.input_file,
        output_file=args.output_file
    )

