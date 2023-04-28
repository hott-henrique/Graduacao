from ODEs.base import ODE

import numpy as np


class SIRS(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(SIRS, self).__init__(initial_condition)

        if self.initial_condition is not None:
            self.N = np.sum(self.initial_condition)

    def do_step(self, t: np.float64, y: np.ndarray, alpha: np.float64, beta: np.float64, gamma: np.float64) -> np.ndarray:
        S, I, R = y

        dSdt = -beta * S * I + alpha * R
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I - alpha * R

        return np.array([ dSdt, dIdt, dRdt ])

    def calculate_error(self, experimental_data: np.ndarray, simulation_data: np.ndarray) -> np.float64:
        l = list()

        for S, I in experimental_data:
            R = self.N - (S + I)

            l.append([ S, I, R ])

        experimental_data = np.array(l)

        return super(SIRS, self).calculate_error(experimental_data, simulation_data)

