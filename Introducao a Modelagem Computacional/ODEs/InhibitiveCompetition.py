from ODEs.base import ODE

import numpy as np


class InhibitiveCompetition(ODE):

    def __init__(self, initial_condition: None | np.ndarray = None):
        super(InhibitiveCompetition, self).__init__(initial_condition)
        pass

    def do_step(
            self,
            t: np.float64,
            y: np.ndarray,
            k1: np.float64,
            k2: np.float64,
            k3: np.float64,
            k4: np.float64,
            k5: np.float64
        ) -> np.ndarray:
        S, E, I, ES, EI, P = y

        dSdt = ES * k2 \
             - S * E * k1

        dEdt = ES * k2 \
             + ES * k3 \
             + EI * k5 \
             - S * E * k1 \
             - E * I * k4
        
        dESdt = S * E * k1 \
              - ES * k2 \
              - ES * k3

        dPdt = ES * k3

        dIdt = EI * k5 \
             - E * I * k4

        dEIdt = E * I * k4 \
              - EI * k5

        return np.array([ dSdt, dEdt, dIdt, dESdt, dEIdt, dPdt ])

