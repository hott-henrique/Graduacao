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

csv_s: list[StringIO] = PIPE()

sims, n = list(), 0

for file in csv_s:
    data = np.loadtxt(file, delimiter=',')

    if len(data) > n:
        n = len(data)

    sims.append(data)

expanded_sims = list()

for data in sims:
    diff = n - data.shape[0]

    missing = np.full(shape=(diff, 4), fill_value=data[-1])

    expanded_sims.append(np.vstack([ data, missing ]))

# Three dimensional matrix: Array of 2D Matrices representing a simulation.

# simulations = np.array([ np.loadtxt(f, delimiter=',') for f in csv_s ])
simulations = np.array(expanded_sims)

#   Tranposing it pull apart each component of simulation in a different matrix,
# where each row of the inner matrices represent an instant in time, and the each value
# corresponde to its simulation. Example with four simulations:
# [ [ 0, 0, 0, 0 ]
#   [ 1, 1, 1, 1 ]
#   [ 2, 2, 2, 2 ]
#   [ 3, 3, 3, 3 ] ]
# The time matrix, each column is a simulation and each row is an instant in time.
transposed = simulations.transpose()

# Remove the time matrix.
data = np.array([ transposed[i] for i in range(1, len(transposed))])

# Two dimensional matrix: row compoment mean over time.
# Example: m[0][0] - Mean of S in the first iteration.
m, s = np.mean(data, axis=2), np.std(data, axis=2)

# PLOTTING --------------------------------------------------

fig, ax = plt.subplots(nrows=1, ncols=3)

fig.set_size_inches((10, 6))

for s in simulations:
    steps = s[:, 0]

    for i in range(1, s.shape[1]):
        ax[i - 1].plot(steps, s[:, i])

fig.savefig("test.png")


