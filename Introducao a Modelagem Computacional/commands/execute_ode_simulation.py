# ODE
import numpy as np

import ODEs
import Solvers


def execute_ode_simulation(ode_config, simulation_config):
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

