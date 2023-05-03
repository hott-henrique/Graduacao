import argparse, contextlib, sys, os, random

from typing import Callable

import numpy as np


def writer(fn): 
    @contextlib.contextmanager
    def stdout():
        yield sys.stdout

    return open(fn, 'w') if fn else stdout()

def simulate(
        y0: np.ndarray,
        propensities: list[Callable],
        stoichiometry: np.ndarray,
        tf: np.float64,
    ):
    steps = [ np.float64(0.0) ]
    simulation_data = [ y0 ]

    ti, yi = steps[-1], simulation_data[-1]

    while ti < tf:
        rates = [ prop(*yi) for prop in propensities ]

        if not any(rates):
            break

        transition = random.choices(stoichiometry, weights=rates)[0]

        yi = np.array([ x + y for x, y in zip(yi, transition) ])

        dt = random.expovariate(np.sum(rates))

        ti = ti + dt

        steps.append(ti)
        simulation_data.append(yi)

    return steps, simulation_data


def main(
        y0: np.ndarray,
        ode_params: np.ndarray,
        tf: np.float64,
        output_file: str,
    ):
    alpha, beta, gamma, rho, epsilon, eta = ode_params
    # alpha    : R -> S
    # beta     : Disease Transimission
    # gamma    : Recovery
    # rho      : Birth
    # epsilon  : Death
    # eta      : Vaccination

    beta = 2
    gamma = 0.5

    N = np.sum(y0)

    V = y0[0] * eta

    y0[0] = y0[0] - V # Vaccination

    # iDIVn = I / N
    # dSdt = rho * N - beta * S * iDIVn + alpha * R
    # dIdt = beta * S * iDIVn - gamma * I - epsilon * I
    # dRdt = gamma * I - alpha * R

    propensities = [
        lambda s, i, r: beta * s * i / N,   # S -> I, Propensity: b * S(t) * I(t) / N
        lambda s, i, r: gamma * i,          # I -> R, Propensity: g * I(t)
        lambda s, i, r: rho * (s + i + r + V),
        lambda s, i, r: epsilon * i,
        lambda s, i, r: alpha * r,
    ]

    stoichiometry = np.array([
        [-1,  1,  0],     # S -> I, Population change: S - 1, I + 1, R + 0
        [ 0, -1,  1],     # I -> R,  Population change: S + 0, I - 1, R + 1
        [+1,  0,  0],
        [ 0, -1,  0],
        [+1,  0, -1],
    ])

    steps, simulation_data = simulate(
        y0=y0,
        propensities=propensities,
        stoichiometry=stoichiometry,
        tf=tf
    )

    with writer(output_file) as f:
        for ti, (Si, Ii, Ri) in zip(steps, simulation_data):
            print(','.join([ str(ti), str(Si), str(Ii), str(Ri) ]), file=f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--y0", required=True, nargs='+', type=np.float64)
    parser.add_argument("--ode-params", required=True, nargs='+', type=np.float64)
    parser.add_argument("--tf", required=True, type=np.float64)
    parser.add_argument("--output-file", required=False, default='')

    args = parser.parse_args()

    dirs = os.path.dirname(args.output_file)

    if dirs:
        os.makedirs(dirs, exist_ok=True)

    main(
        y0=args.y0,
        ode_params=args.ode_params,
        tf=args.tf,
        output_file=args.output_file,
    )

