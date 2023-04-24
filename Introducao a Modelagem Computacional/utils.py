import typing as t

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def euler(
		func: t.Callable,
		tk: t.SupportsFloat,
		_yk: np.ndarray,
		_dt: t.SupportsFloat = 0.01,
		**kwargs
	):
	"""
	single-step euler method
	func: system of first order ODEs
	tk: current time step
	_yk: current state vector [y1, y2, y3, ...]
	_dt: discrete time step size
	**kwargs: additional parameters for ODE system
	returns: y evaluated at time k+1
	"""
	return _yk + func(tk, _yk, **kwargs)*_dt

def rk4(
		func: t.Callable,
		tk: t.SupportsFloat,
		_yk: np.ndarray,
		_dt: t.SupportsFloat = 0.01,
		**kwargs
	):
	"""
	single-step fourth-order numerical integration (RK4) method
	func: system of first order ODEs
	tk: current time step
	_yk: current state vector [y1, y2, y3, ...]
	_dt: discrete time step size
	**kwargs: additional parameters for ODE system
	returns: y evaluated at time k+1
	"""

	# Evaluate derivative at several stages within time interval
	f1 = func(tk, _yk, **kwargs)
	f2 = func(tk + _dt / 2, _yk + (f1 * (_dt / 2)), **kwargs)
	f3 = func(tk + _dt / 2, _yk + (f2 * (_dt / 2)), **kwargs)
	f4 = func(tk + _dt, _yk + (f3 * _dt), **kwargs)

	# Return an average of the derivative over tk, tk + dt
	return _yk + (_dt / 6) * (f1 + (2 * f2) + (2 * f3) + f4)

def simulate(
		ode_system: t.Callable,
		initial_condition: np.ndarray,
		delta_t: t.SupportsFloat,
		t_final: t.SupportsFloat,
		solver: t.Callable,
		ode_system_kwargs: t.Dict = dict(),
	) -> t.Tuple[np.ndarray[float], np.ndarray]:
	t_final = float(t_final)
	delta_t = float(delta_t)

	time_steps = np.arange(0, t_final + delta_t, delta_t)

	state_history = list()

	yk = initial_condition

	for t in time_steps:
		state_history.append(yk)

		yk = solver(
			func=ode_system,
			tk=t,
			_yk=yk,
			_dt=delta_t,
			**ode_system_kwargs
		)

	return time_steps, np.array(state_history)

def save_simulation(
		time_steps: np.ndarray,
		state_history: np.ndarray,
		columns_labels: t.Iterable[t.AnyStr],
		file_path: t.AnyStr
	) -> None:
	df = pd.DataFrame(state_history, columns=columns_labels)
	df.insert(0, "Time", time_steps)
	df.to_csv(file_path, float_format='%.5f', sep=',', index=False) 

def plot_simulation(
		time_steps: np.ndarray,
		state_history: np.ndarray,
		xlabel: t.AnyStr,
		ylabel: t.AnyStr,
		title: t.AnyStr,
		columns_to_plot: t.Iterable[t.SupportsInt],
		columns_labels: t.Iterable[t.AnyStr],
		figure_path: t.AnyStr
	):
	fig, ax = plt.subplots()

	fig.set_size_inches(8, 6)

	ax.grid()
	ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

	ax.plot(time_steps, state_history[:, columns_to_plot], label=columns_labels)

	ax.legend()

	fig.savefig(figure_path)
