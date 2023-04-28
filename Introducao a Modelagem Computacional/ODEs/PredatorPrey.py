from ODEs.base import ODE

import numpy as np


class PredatorPrey(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(PredatorPrey, self).__init__(initial_condition)

    def do_step(
            self,
            t: np.float64,
            y: np.ndarray,
            a: np.float64, b: np.float64,
            r: np.float64, m: np.float64
        ) -> np.ndarray:
        Py, Pr = y

        dHdt = Py * r - Py * Pr * a
        dPdt = Py * Pr * b - Pr * m

        return np.array([ dHdt, dPdt ])

