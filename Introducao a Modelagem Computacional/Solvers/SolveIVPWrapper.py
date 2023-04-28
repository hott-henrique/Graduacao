import scipy


def solve_ivp(fun, args, y0, t_span, t_eval):
    return scipy.integrate.solve_ivp(
        fun=fun,
        args=args,
        t_span=t_span,
        y0=y0,
        t_eval=t_eval
    ).y

