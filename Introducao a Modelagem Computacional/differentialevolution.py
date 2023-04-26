import numpy as np
import scipy

from odes import ode_sirs

def simulate_ode(ode_params, *simulation_params):
    ground_truth_data, steps, t_indices_pairing, initial_condition = simulation_params

    results = scipy.integrate.solve_ivp(
        fun=ode_sirs,
        args=ode_params,
        t_span=(0, np.max(steps)),
        y0=initial_condition,
        t_eval=steps,
        method="RK45"
    )

    S, I = results.y[[ 0, 1 ], :]

    errorS, errorI = 0, 0
    sumS, sumI = 0, 0

    for experimental_index, simulation_index in t_indices_pairing:
        truthS = ground_truth_data[experimental_index][1]
        truthI = ground_truth_data[experimental_index][2]

        errorS = errorS + np.float_power((S[simulation_index] - truthS), 2)
        errorI = errorI + np.float_power((I[simulation_index] - truthI), 2)

        sumS = sumS + truthS
        sumI = sumI + truthI

    error = np.sqrt(errorS / sumS) \
          + np.sqrt(errorI / sumI)

    return error

if __name__ == "__main__":
    ground_truth_data = np.loadtxt(".local/parameter_adjustment_data.csv", delimiter=',')

    tf, dt = 10, 0.01

    simulation_timestamps = np.arange(0, tf + dt, dt)

    t_indices_pairing = list()

    search_starting_point = 0

    for i, t_experimental in enumerate(ground_truth_data[:, 0]):

        for j in range(search_starting_point, len(simulation_timestamps)):
            t_simulation = simulation_timestamps[j]

            if np.abs(t_experimental - t_simulation) <= dt:
                t_indices_pairing.append((i, j))
                search_starting_point = j + 1
                break

    t_indices_pairing = np.array(t_indices_pairing)

    simulation_params = (
        ground_truth_data,
        simulation_timestamps,
        t_indices_pairing,
        np.array([ 995, 5, 0 ], dtype=np.float64)
    )

    bounds = [ (0.1, 0.3), (0.01, 0.02), (0.5, 1) ]

    solution = scipy.optimize.differential_evolution(
        func=simulate_ode,
        args=simulation_params,
        bounds=bounds,
        strategy="best1bin",
        maxiter=30,
        popsize=80,
        atol=10**(-3),
        tol=10**(-3),
        mutation=0.8,
        recombination=0.5,
        workers=4,
        updating="deferred",
        disp=True,
    )

    best_params = solution.x
    error = simulate_ode(best_params, *simulation_params)

    print(f"Best Solution: {best_params}")
    print(f"Error: {error}")
    print(f"{solution.message}")

