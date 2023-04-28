from ODEs.base import ODE

import numpy as np


class SIRS(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(SIRS, self).__init__(initial_condition)

    def do_step(self, t: np.float64, y: np.ndarray, alpha: np.float64, beta: np.float64, gamma: np.float64) -> np.ndarray:
        S, I, R = y

        dSdt = -beta * S * I + alpha * R
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I - alpha * R

        return np.array([ dSdt, dIdt, dRdt ])

