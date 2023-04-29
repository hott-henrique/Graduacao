import argparse, contextlib, sys, os

import numpy as np

import ode


def writer(fn): 
    @contextlib.contextmanager
    def stdout():
        yield sys.stdout

    return open(fn, 'w') if fn else stdout()

def euler(func, ti, yi, dt, *args):
    return yi + func(ti, yi, *args) * dt

def rk4(func, ti, yi, dt, *args):
    f1 = func(ti, yi, *args)
    f2 = func(ti + dt / 2, yi + (f1 * (dt / 2)), *args)
    f3 = func(ti + dt / 2, yi + (f2 * (dt / 2)), *args)
    f4 = func(ti + dt, yi + (f3 * dt), *args)

    return yi + (dt / 6) * (f1 + (2 * f2) + (2 * f3) + f4)

def main(
        # Simulation Args
        tf, dt, solver,

        # ODE Args
        y0, ode_params,

        # Output Args
        output_file: str = ""
    ):
    steps = np.arange(0, tf + dt, dt)

    data = list()

    yi = y0

    for ti in steps:
        data.append(yi)

        yi = solver(ode.ABC, ti, yi, dt, *ode_params)

    with writer(output_file) as f:
        for dt, [ a, b, c ] in zip(steps, data):
            values = np.array([ dt, a, b, c ]).round(4)

            s =','.join([ str(v) for v in values ]) + '\n'

            f.write(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--tf", required=True, type=np.float64)
    parser.add_argument("--dt", required=True, type=np.float64)
    parser.add_argument("--solver", required=True, choices=[ "euler", "rk4" ])
    parser.add_argument("--y0", required=True, nargs='+', type=np.float64)
    parser.add_argument("--ode-params", required=True, nargs='+', type=np.float64)
    parser.add_argument("--output-file", required=False, default='')

    args = parser.parse_args()

    dirs = os.path.dirname(args.output_file)

    if dirs:
        os.makedirs(dirs, exist_ok=True)

    main(
        tf=args.tf,
        dt=args.dt,
        solver=locals()[args.solver],
        y0=np.array(args.y0),
        ode_params=np.array(args.ode_params),
        output_file=args.output_file
    )

