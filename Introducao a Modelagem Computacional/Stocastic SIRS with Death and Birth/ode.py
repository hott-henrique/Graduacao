import numpy as np


def SIRS(
        t: np.float64,
        y: np.ndarray,
        alpha: np.float64,
        beta: np.float64,
        gamma: np.float64,
        rho: np.float64, # Birth rate
        epsilon: np.float64 # Mortality rate
    ) -> np.ndarray:
    S, I, R = y

    N = np.sum(y)

    iDIVn = I / N

    dSdt = rho * N - beta * S * iDIVn + alpha * R
    dIdt = beta * S * iDIVn - gamma * I - epsilon * I
    dRdt = gamma * I - alpha * R

    return np.array([ dSdt, dIdt, dRdt ])

