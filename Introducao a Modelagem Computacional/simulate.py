import argparse

import numpy as np

import ODEs
import Solvers


def main(ode_config, simulation_config):
    ode_name = ode_config["ode"]
    initial_condition = ode_config["initial_condition"]
    parameters = ode_config["parameters"]

    tf = simulation_config["tf"]
    dt = simulation_config["dt"]
    solver_name = simulation_config["solver"]

    ode: ODEs.ODE = getattr(ODEs, ode_name)(initial_condition)

    solver = getattr(Solvers, solver_name)

    steps, y = ode.simulate(
        tf=tf,
        dt=dt,
        solver=solver,
        ode_parameters=parameters
    )

    for t, yt in zip(steps,y.T):
        row = [ t, *yt ]
        print(','.join([ str(np.round(v, 4)) for v in row ]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--ode", type=str, required=True)
    parser.add_argument("--initial-condition", type=float, nargs="+", required=True)
    parser.add_argument("--parameters", type=float, nargs="+", required=True)

    parser.add_argument("--solver", type=str, default="solve_ivp")
    parser.add_argument("--tf", type=float, required=True)
    parser.add_argument("--dt", type=float, required=True)

    arguments = parser.parse_args()

    ode_config = {
        "ode": arguments.ode,
        "initial_condition": np.array(arguments.initial_condition, dtype=np.float64),
        "parameters": np.array(arguments.parameters, dtype=np.float64),
    }

    simulation_config = {
        "solver": arguments.solver,
        "tf": np.float64(arguments.tf),
        "dt": np.float64(arguments.dt),
    }

    main(ode_config, simulation_config)

