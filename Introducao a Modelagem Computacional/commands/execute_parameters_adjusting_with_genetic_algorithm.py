import numpy as np

import ODEs
import Solvers
import Fitting


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

def simulate(ode: ODEs.base.ODE, ode_parameters: np.ndarray, *simulation_params):
    experimental_data, tf, dt, solver = simulation_params

    steps, results = ode.simulate(
        tf=tf,
        dt=dt,
        solver=solver,
        ode_parameters=ode_parameters,
    )

    for row in results:
        row: np.ndarray = row

        if np.any(np.isnan(row)):
            return np.inf

    pairing_indices = get_pairing_indices(experimental_data[:, 0], steps)

    experimental_indices = pairing_indices[:, 0]
    simulation_indices = pairing_indices[:, 1]

    e = ode.calculate_error(
        experimental_data=experimental_data[:, 1:][experimental_indices],
        simulation_data=results[:, simulation_indices].T
    )

    return e

def execute_parameters_adjusting_with_genetic_algorithm(
        experimental_data_file_path,

        ode,
        bounds,
        initial_condition,

        G,
        P,
        mutation,

        tf,
        dt,
        solver,

        output_file
    ):
    experimental_data = np.loadtxt(experimental_data_file_path, delimiter=',')

    simulation_params = (
        experimental_data,
        tf,
        dt,
        getattr(Solvers, solver)
    )

    ode = getattr(ODEs, ode)(initial_condition=initial_condition)

    ga = Fitting.GeneticAlgorithm(
        bounds=bounds,
        func=lambda ode_params, *args: simulate(ode, ode_params, *args),
        ode=ode,
        args=simulation_params,
        fitness_as_error=True
    )

    best_params, _ = ga.evolution(P=P, G=G, mutation=mutation)

    with open(output_file, 'w') as f:
        print(' '.join([ str(v) for v in best_params ]), file=f)

