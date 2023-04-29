import numpy as np


def SIRS(t: np.float64, y: np.ndarray, alpha: np.float64, beta: np.float64, gamma: np.float64) -> np.ndarray:
    S, I, R = y

    dSdt = -beta * S * I + alpha * R
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I - alpha * R

    return np.array([ dSdt, dIdt, dRdt ])

