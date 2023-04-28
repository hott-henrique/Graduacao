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

def plot_csv(**kwargs):
    plot(
        simulation_data=load_simulation(kwargs.pop("csv_file")),
        output_file=kwargs.pop("output_file"),
        **kwargs if kwargs else dict()
    )
