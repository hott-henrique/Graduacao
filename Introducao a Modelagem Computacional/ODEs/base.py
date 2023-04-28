from abc import ABC, abstractmethod

import numpy as np


class ODE(ABC):

    @abstractmethod
    def __init__(self, initial_condition: None | np.ndarray = None):
        self.initial_condition = initial_condition

    @abstractmethod
    def do_step(self, *args, **kwargs) -> np.ndarray:
        pass

    def simulate(self, tf, dt, solver, ode_parameters: list = list()) -> tuple[np.ndarray, np.ndarray]:
        if self.initial_condition is None:
            raise Exception("Impossible to simulate ODE without initial condition.")

        tf = np.float64(tf)
        dt = np.float64(dt)

        steps = np.arange(0, tf + dt, dt)

        y = solver(
            fun=self.do_step,
            args=ode_parameters,
            t_span=(0, tf + dt),
            y0=self.initial_condition,
            t_eval=steps,
        )

        return steps, y

    def calculate_errors(self, experimental_data: np.ndarray, simulation_data: np.ndarray):
        errors = np.zeros(shape=experimental_data.shape[1])
        exacts = np.zeros(shape=experimental_data.shape[1])

        for experimental, simulation in zip(experimental_data, simulation_data):
            errors = errors + np.float_power(simulation - experimental, 2)
            exacts = exacts + np.float_power(experimental, 2)

        return np.sum(np.sqrt(errors / exacts))

