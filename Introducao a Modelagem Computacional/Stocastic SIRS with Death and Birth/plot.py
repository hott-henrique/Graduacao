import argparse, os
from io import StringIO

import numpy as np
from matplotlib import pyplot as plt


def PIPE() -> list[StringIO]:
    container, csv = list(), list()

    while True:
        try:
            s = input()

            if not s:
                container.append(StringIO('\n'.join(csv)))
                csv.clear()
                continue

            csv.append(s)
        except:
            break;

    return container

def calculate_average(simulations: list[np.ndarray]):
    N = simulations[0].shape[0]
    for i in range(1, len(simulations)):
        m = simulations[i].shape[0]

        if m < N:
            N = m

    avgt = np.zeros(shape=N)
    avgS = np.zeros(shape=N)
    avgI = np.zeros(shape=N)
    avgR = np.zeros(shape=N)

    for s in simulations:
        avgt = avgt + s[:N, 0]
        avgS = avgS + s[:N, 1]
        avgI = avgI + s[:N, 2]
        avgR = avgR + s[:N, 3]

    avgt = avgt / len(simulations)
    avgS = avgS / len(simulations)
    avgI = avgI / len(simulations)
    avgR = avgR / len(simulations)

    return avgt, avgS, avgI, avgR

def plot(output_file: str):
    csv_s: list[StringIO] = PIPE()

    simulations = [ np.loadtxt(file, delimiter=',') for file in csv_s ]

    fig, ax = plt.subplots(nrows=1, ncols=3)

    fig.set_size_inches((14, 6))

    color_sim = 0.0

    for s in simulations:
        steps = s[:, 0]

        ax[0].plot(steps, s[:, 1], color=(color_sim, color_sim, color_sim))
        ax[1].plot(steps, s[:, 2], color=(color_sim, color_sim, color_sim))
        ax[2].plot(steps, s[:, 3], color=(color_sim, color_sim, color_sim))

        ax[0].set_title("[ S ]")
        ax[1].set_title("[ I ]")
        ax[2].set_title("[ R ]")


        color_sim += 0.125

    avgt, avgS, avgI, avgR = calculate_average(simulations)

    ax[0].plot(avgt, avgS, color='r')
    ax[1].plot(avgt, avgI, color='r')
    ax[2].plot(avgt, avgR, color='r')

    fig.savefig(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--output-file", required=True)

    args = parser.parse_args()

    dirs = os.path.dirname(args.output_file)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    plot(args.output_file)

