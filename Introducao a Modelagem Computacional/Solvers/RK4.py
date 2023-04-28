import numpy as np


def rk4(fun, args, y0, t_span, t_eval):
    dt = (t_span[1] - t_span[0]) / len(t_eval)

    yk = y0

    results = [ list() for _ in range(len(y0)) ]

    for t in t_eval:
        for container, value in zip(results, yk):
            container.append(value)

        f1 = fun(t, yk, *args)
        f2 = fun(t + dt / 2, yk + (f1 * (dt / 2)), *args)
        f3 = fun(t + dt / 2, yk + (f2 * (dt / 2)), *args)
        f4 = fun(t + dt, yk + (f3 * dt), *args)

        yk = yk + (dt / 6) * (f1 + (2 * f2) + (2 * f3) + f4)

    return np.array(results)

