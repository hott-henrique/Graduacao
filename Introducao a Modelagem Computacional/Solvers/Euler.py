import numpy as np


def euler(fun, args, y0, t_span, t_eval):
    dt = (t_span[1] - t_span[0]) / len(t_eval)

    yk = y0

    results = [ list() for _ in range(len(y0)) ]

    for t in t_eval:
        for container, value in zip(results, yk):
            container.append(value)

        yk = yk + fun(t, yk, *args) * dt

    return np.array(results)

