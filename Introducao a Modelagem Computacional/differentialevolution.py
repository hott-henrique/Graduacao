import numpy as np
import scipy

from odes import ode_sirs

def simulate_ode(ode_params, *simulation_params):
    ground_truth_data, steps, indices, initial_condition = simulation_params

    results = scipy.integrate.solve_ivp(
        fun=ode_sirs,
        args=ode_params,
        t_span=(0, np.max(steps)),
        y0=initial_condition,
        t_eval=steps,
        method="RK45"
    )

    S = results.y[0, :]
    I = results.y[1, :]
    R = results.y[2, :]

    errorS, errorI, errorR = 0, 0, 0
    sumS, sumI, sumR = 0, 0, 0

    for ground_truth_index, simulation_index in enumerate(indices):
        truthS = ground_truth_data[ground_truth_index][1]
        truthI = ground_truth_data[ground_truth_index][2]
        truthR = 1000 - (truthS + truthI)

        errorS = errorS + np.float_power((S[simulation_index] - truthS), 2)
        errorI = errorI + np.float_power((I[simulation_index] - truthI), 2)
        errorR = errorR + np.float_power((R[simulation_index] - truthR), 2)

        sumS = sumS + truthS
        sumI = sumI + truthI
        sumR = sumR + truthR

    error = np.sqrt(errorS / sumS) \
          + np.sqrt(errorI / sumI) \
          + np.sqrt(errorR / sumR)

    return error

if __name__ == "__main__":
    ground_truth_data = np.loadtxt(".local/parameter_adjustment_data.csv", delimiter=',')

    tf, dt = 50, 0.01

    simulation_timestamps = np.arange(0, tf + dt, dt)

    simulation_params = (
        ground_truth_data,
        simulation_timestamps,
        np.digitize(ground_truth_data[:, 0], simulation_timestamps),
        np.array([ 995, 0, 0.05 ], dtype=np.float64)
    )

    results = scipy.integrate.solve_ivp(
        fun=ode_sirs,
        args=np.array([ 0.01, 1.25, 2.25 ]),
        t_span=(0, np.max(simulation_params[1])),
        y0=simulation_params[3],
        t_eval=simulation_params[1],
        method="RK45"
    )

    # print(results.y[0, :])

    # exit(0)

    bounds = [ (0.01, 5), (0.01, 5), (0.01, 5) ]

    solution = scipy.optimize.differential_evolution(
        func=simulate_ode,
        args=simulation_params,
        bounds=bounds,
        strategy="best1bin",
        maxiter=10,
        popsize=20,
        atol=10**(-3),
        tol=10**(-3),
        mutation=0.8,
        recombination=0.5,
        disp=True,
    )

    best_params = solution.x
    error = simulate_ode(best_params, *simulation_params)

    if solution.success:
        print(f"Best Solution: {best_params}")
        print(f"Error: {error}")
    else:
        print(f"{solution.message}")

