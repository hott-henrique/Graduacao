import argparse, contextlib, sys, os

import numpy as np
import scipy

import ode

from GeneticAlgorithm import GeneticAlgorithm


CLI = argparse.ArgumentParser()

SUBPARSERS = CLI.add_subparsers(dest="subcommand")

def subcommand(args=[], parent=SUBPARSERS, **kwargs):
    def decorator(func):
        parser = parent.add_parser(
            kwargs.pop("command_name", func.__name__), description=func.__doc__
        )

        for arg in args:
            parser.add_argument(*arg[0], **arg[1])

        parser.set_defaults(func=func)

    return decorator

def argument(*name_or_flags, **kwargs):
    return ([*name_or_flags], kwargs)

def calculate_sirs_model_error(ode_params, *args) -> np.float64:
    experimental_data, tf, dt, y0 = args

    N = np.sum(y0)

    sim_steps = np.arange(0, tf + dt, dt)

    data = scipy.integrate.solve_ivp(
        fun=ode.SIRS,
        t_span=(0, tf + dt),
        y0=y0,
        t_eval=sim_steps,
        args=ode_params
    ).y

    errorS, errorI, errorR = 0, 0, 0
    exactS, exactI, exactR = 0, 0, 0

    i = np.int64(-1)
    for t_exp, truthS, truthI in experimental_data:
        for j in range(i + 1, len(sim_steps)):
            t_sim = sim_steps[j]

            if np.abs(t_exp - t_sim) > dt:
                continue

            i = j
            break;

        simS = data[0][i]
        simI = data[1][i]
        simR = data[2][i]

        truthR = N - (truthS + truthI)

        errorS += np.float_power(simS - truthS, 2)
        errorI += np.float_power(simI - truthI, 2)
        errorR += np.float_power(simR - truthR, 2)

        exactS += np.float_power(truthS, 2)
        exactI += np.float_power(truthI, 2)
        exactR += np.float_power(truthR, 2)

    return np.sum([
        np.sqrt(errorS / exactS),
        np.sqrt(errorI / exactI),
        np.sqrt(errorR / exactR)
    ])

def bounds(arg):
    try:
        l = list()

        for bound in arg.split('/'):
            i, s = bound.split('-')
            b = (np.float64(i), np.float64(s))
            l.append(b)

        return l
    except:
        raise argparse.ArgumentTypeError("Bounds must be like: I0-S0/.../Ii-Si")

def pint(arg):
    n = np.int64(arg)

    if n <= 0:
        raise argparse.ArgumentTypeError("G must be an integer number greater than one.")

    return n

def pint_even(arg):
    try:
        n = pint(arg)

        if n % 2 != 0:
            raise ValueError()
    except:
        raise argparse.ArgumentTypeError("Must be an even integer number greater than one.")

    return n

def mutation(arg):
    m = np.float64(arg)

    if m < 0 or 1 < m:
        raise argparse.ArgumentTypeError("Must be a float number in range [0, 1]")

    return m

def recombination(arg):
    m = np.float64(arg)

    if m < 0 or 1 < m:
        raise argparse.ArgumentTypeError("Must be a float number in range [0, 1]")

    return m

def writer(fn): 
    @contextlib.contextmanager
    def stdout():
        yield sys.stdout

    return open(fn, 'w') if fn else stdout()

@subcommand(
    [
        argument("--bounds", type=bounds, required=True),
        argument("--y0", type=np.float64, nargs="+", required=True),

        argument("--experimental-data", help="Path to experimental data for the ode model.", required=True),

        argument("--mutation", type=mutation, required=True),
        argument("--recombination", type=recombination, required=True),
        argument("--maxiter", type=pint, required=True),
        argument("--popsize", type=pint_even, required=True),

        argument("--tf", type=np.float64, required=True),
        argument("--dt", type=np.float64, required=True),

        argument("--output-file", type=str, required=False)
    ],
    command_name="de",
)
def execute_differential_evolution(args):
    experimental_data = np.loadtxt(args.experimental_data, delimiter=',')
    
    best_params = scipy.optimize.differential_evolution(
        func=calculate_sirs_model_error,
        args=(experimental_data, args.tf, args.dt, np.array(args.y0)),
        bounds=args.bounds,
        strategy="best1bin",
        maxiter=args.maxiter,
        popsize=args.popsize,
        atol=0.0001,
        tol=0.0001,
        mutation=args.mutation,
        recombination=args.recombination,
        disp=True,
        workers=4,
        updating="deferred"
    ).x

    dirs = os.path.dirname(args.output_file)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    with writer(args.output_file) as f:
        print(','.join([ str(p) for p in best_params ]), file=f)

@subcommand(
    [
        argument("--experimental-data", help="Path to experimental data for the ode model.", required=True),

        argument("--tf", type=np.float64, required=True),
        argument("--dt", type=np.float64, required=True),

        argument("--y0", type=float, nargs="+", required=True),
        argument("--bounds", type=bounds, required=True),

        argument("--G", type=pint, required=True),
        argument("--P", type=pint_even, required=True),
        argument("--mutation", type=float, required=True),

        argument("--output-file", type=str, required=False)
    ],
    command_name="ga",
)
def execute_genetic_algorithm(args):
    experimental_data = np.loadtxt(args.experimental_data, delimiter=',')

    ga = GeneticAlgorithm(
        bounds=args.bounds,
        func=calculate_sirs_model_error,
        args=(experimental_data, args.tf, args.dt, np.array(args.y0)),
        fitness_as_error=True
    )

    best_params , _ = ga.evolution(P=args.P, G=args.G, mutation=args.mutation)

    dirs = os.path.dirname(args.output_file)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    with writer(args.output_file) as f:
        print(','.join([ str(p) for p in best_params ]), file=f)

if __name__ == "__main__":
    args = CLI.parse_args()

    args.func(args) if args.subcommand is not None else CLI.print_help()

