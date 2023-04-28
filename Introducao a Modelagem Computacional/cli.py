import argparse

import numpy as np

import commands

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

def arg_bounds(arg):
    try:
        l = list()

        for bound in arg.split('/'):
            i, s = bound.split('-')
            l.append(( float(i), float(s) ))

        return l
    except:
        raise argparse.ArgumentTypeError("Bounds must be like: I1-S1/I2-S2")

def arg_population(arg):
    try:
        arg = int(arg)
        
        if arg % 2 != 0:
            raise ValueError()

        return arg
    except:
        raise argparse.ArgumentTypeError("Population size must be an integer and multiple of two.")

def arg_generations(arg):
    try:
        arg = int(arg)
        
        if arg < 1:
            raise ValueError()

        return arg
    except:
        raise argparse.ArgumentTypeError("Number of generations must be an integer and greater than zero.")

@subcommand(
    [
        argument("--ode", type=str, required=True),
        argument("--parameters", type=float, nargs="+", required=True),

        argument("--initial-condition", type=float, nargs="+", required=True),

        argument("--solver", type=str, default="solve_ivp"),
        argument("--tf", type=float, required=True),
        argument("--dt", type=float, required=True),
    ],
    command_name="execute-ode-simulation"
)
def execute_ode_simulation(args):
    ode_config = {
        "ode": args.ode,
        "initial_condition": np.array(args.initial_condition, dtype=np.float64),
        "parameters": np.array(args.parameters, dtype=np.float64),
    }

    simulation_config = {
        "solver": args.solver,
        "tf": np.float64(args.tf),
        "dt": np.float64(args.dt),
    }

    commands.execute_ode_simulation(ode_config, simulation_config)

@subcommand(
    [
        argument("--csv-file", type=str, required=False, default='', help="File to read csv. If not specified, read from stding untill EOF."),
        argument("--output-file", type=str, required=True),
        argument("--title", type=str, required=False),
        argument("--xlabel", type=str, required=False),
        argument("--ylabel", type=str, required=False),
        argument("--labels", type=str, nargs="*", required=False, help="Label for each line in plot. If specified, it must have one element for each column in file, even if not ploting all columns."),
        argument("--columns", type=int, nargs="*", required=False, default=list(), help="Plot only specified columns."),
    ],
    command_name="plot-csv"
)
def plot_csv(args):
    commands.plot_csv(
        csv_file=args.csv_file,
        title=args.title,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
        labels=args.labels,
        columns=args.columns,
        output_file=args.output_file,
    )

@subcommand(
    [
        argument("--ode", type=str, required=True),
        argument("--bounds", type=arg_bounds, required=True),

        argument("--experimental-data", help="Path to experimental data for the ode model.", required=True),
        argument("--initial-condition", type=float, nargs="+", required=True),

        argument("--G", type=arg_generations, required=True),
        argument("--P", type=arg_population, required=True),
        argument("--mutation", type=float, required=True),

        argument("--tf", type=float, required=True),
        argument("--dt", type=float, required=True),
        argument("--solver", type=str, required=False, default="solve_ivp"),

        argument("--output-file", type=str, required=True)
    ],
    command_name="parameters-adjusment-ga",
)
def execute_genetic_algorithm(args):
    commands.execute_parameters_adjusting_with_genetic_algorithm(
        experimental_data_file_path = args.experimental_data,
        initial_condition = np.array(args.initial_condition, dtype=np.float64),

        ode = args.ode,
        bounds = args.bounds,

        G = args.G,
        P = args.P,
        mutation = args.mutation,

        tf = args.tf,
        dt = args.dt,
        solver = args.solver,

        output_file = args.output_file,
    )


if __name__ == "__main__":
    args = CLI.parse_args()

    args.func(args) if args.subcommand is not None else CLI.print_help()

