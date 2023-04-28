from ODEs.base import ODE

import numpy as np


class Competition(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(Competition, self).__init__(initial_condition)

    def do_step(
            self,
            t: np.float64,
            y: np.ndarray,
            r1: np.float64, r2: np.float64,
            w11: np.float64, w12: np.float64,
            w21: np.float64, w22: np.float64
        ):
        Sa, Sb = y

        dN1dt = Sa * (1 - Sa * w11 - Sb * w21) * r1
        dN2dt = Sb * (1 - Sb * w22 - Sa * w12) * r2

        return np.array([ dN1dt, dN2dt ])

