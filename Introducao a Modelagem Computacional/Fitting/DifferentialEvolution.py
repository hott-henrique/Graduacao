import argparse

import numpy as np
import scipy

from odes import ode_sirs

def simulate_sirs(ode_params, *simulation_params):
    ground_truth_data, steps, t_indices_pairing, initial_condition = simulation_params

    results = scipy.integrate.solve_ivp(
        fun=ode_sirs,
        args=ode_params,
        t_span=(0, np.max(steps)),
        y0=initial_condition,
        t_eval=steps,
        method="RK45"
    )

    S, I, R = results.y[[ 0, 1, 2 ], :]

    N = np.sum(initial_condition)

    errorS, errorI, errorR = 0, 0, 0
    sumS, sumI, sumR = 0, 0, 0

    for experimental_index, simulation_index in t_indices_pairing:
        truthS = ground_truth_data[experimental_index][1]
        truthI = ground_truth_data[experimental_index][2]
        truthR = N - (truthS + truthI)

        errorS = errorS + np.float_power((S[simulation_index] - truthS), 2)
        errorI = errorI + np.float_power((I[simulation_index] - truthI), 2)
        errorR = errorR + np.float_power((R[simulation_index] - truthR), 2)

        sumS = sumS + np.float_power(truthS, 2)
        sumI = sumI + np.float_power(truthI, 2)
        sumR = sumR + np.float_power(truthR, 2)

    error = np.sqrt(errorS / sumS) \
          + np.sqrt(errorI / sumI) \
          + np.sqrt(errorR / sumR)

    return error

def get_pairing_indices(A: np.ndarray, B: np.ndarray, tolerance: float = np.power(1/10, 2)):
    pairing_indices = list()

    search_starting_point = 0

    for i, valueA in enumerate(A):
        for j in range(search_starting_point, len(B)):
            valueB = B[j]

            if np.abs(valueA - valueB) < tolerance:
                pairing_indices.append((i, j))
                search_starting_point = j + 1
                break

    pairing_indices = np.array(pairing_indices)

    return pairing_indices


def main(experimental_data_file_path: str):
    experimental_data = np.loadtxt(experimental_data_file_path, delimiter=',')

    tf, dt = 10, 0.01

    simulation_timestamps = np.arange(0, tf + dt, dt)

    simulation_params = (
        experimental_data,
        simulation_timestamps,
        get_pairing_indices(experimental_data[:, 0], simulation_timestamps, dt),
        np.array([ 995, 5, 0 ], dtype=np.float64)
    )

    bounds = [ (0.01, 1.0), (0.01, 1.0), (0.1, 1.0) ]

    solution = scipy.optimize.differential_evolution(
        func=simulate_sirs,
        args=simulation_params,
        bounds=bounds,
        strategy="best1bin",
        maxiter=100,
        popsize=100,
        atol=0.0001,
        tol=0.0001,
        mutation=0.8,
        recombination=0.5,
        workers=4,
        updating="deferred",
        disp=True,
    )

    best_params = solution.x
    error = simulate_sirs(best_params, *simulation_params)

    with open("de.parameters") as f:
        print(' '.join([ str(v) for v in best_params ]), file=f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--experimental-data",
        help="Path to experimental data for SIRS ode model.",
        required=True
    )

    args = parser.parse_args()

    main(experimental_data_file_path=args.experimental_data)

