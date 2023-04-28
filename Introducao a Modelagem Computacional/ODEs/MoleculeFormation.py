from ODEs.base import ODE

import numpy as np


class MoleculeFormation(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(MoleculeFormation, self).__init__(initial_condition)

    def do_step(self, t: np.float64, y: np.ndarray, k1: np.float64, k2: np.float64) -> np.ndarray:
        A, B, C = y

        dABdt = C * k2 - A * B * k1
        dCdt = A * B * k1 - C * k2

        return np.array([ dABdt, dABdt, dCdt ])


