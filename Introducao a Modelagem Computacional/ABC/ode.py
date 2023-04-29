import numpy as np

def ABC(t: np.float64, y: np.ndarray, k1: np.float64, k2: np.float64) -> np.ndarray:
    A, B, C = y

    dABdt = C * k2 - A * B * k1
    dCdt = A * B * k1 - C * k2

    return np.array([ dABdt, dABdt, dCdt ])

