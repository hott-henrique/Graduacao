import argparse, contextlib, sys, os

import numpy as np
import scipy

import ode


def writer(fn): 
    @contextlib.contextmanager
    def stdout():
        yield sys.stdout

    return open(fn, 'w') if fn else stdout()

def main(tf, dt, y0, ode_params, output_file):
    steps = np.arange(0, tf + dt, dt)

    data = scipy.integrate.solve_ivp(
        fun=ode.SIRS,
        t_span=(0, tf + dt),
        y0=y0,
        t_eval=steps,
        args=ode_params
    ).y

    with writer(output_file) as f:
        for dt, S, I, R in zip(steps, *data):
            values = np.array([ dt, S, I, R ]).round(4)

            s =','.join([ str(v) for v in values ]) + '\n'

            f.write(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--tf", required=True, type=np.float64)
    parser.add_argument("--dt", required=True, type=np.float64)
    parser.add_argument("--y0", required=True, nargs='+', type=np.float64)
    parser.add_argument("--ode-params", required=True, nargs='+', type=np.float64)
    parser.add_argument("--output-file", required=False, default='')

    args = parser.parse_args()

    if args.output_file:
        os.makedirs(os.path.dirname(args.output_file), exist_ok=True)

    main(
        tf=args.tf,
        dt=args.dt,
        y0=np.array(args.y0),
        ode_params=np.array(args.ode_params),
        output_file=args.output_file
    )

