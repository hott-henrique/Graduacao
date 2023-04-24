import numpy as np
import scipy


def odeSystem(t, u, r, k):

    N = u[0]
    dN_dt = r*N*(1 - N/k)
 
    return [dN_dt]  

def time_is_from_ground_truth(times, ct):
    for t in times: 
        if (abs(ct - t) <= 10**(-5)):
            return True 
    return False

def solve(x):
    global data, timestamps

    dt = 0.01
    tfinal = 50
    times = np.arange(0, tfinal+dt, dt)

    N0 = x[0]
    u = [N0]

    r = x[1]
    k = x[2]
    params = (r, k)
    
    def solveOde(t, y):
        return odeSystem(t, y, *params)

    results = scipy.integrate.solve_ivp(solveOde, (0, tfinal), u, t_eval=times, method='Radau')

    u = results.y[0,:]

    error, sumobs, i, j = 0, 0, 0, 0

    for t in times:
        if time_is_from_ground_truth(timestamps, t):
            Ndata = data[i][1]

            error += (u[j] - Ndata) * (u[j] - Ndata) 
            sumobs += Ndata * Ndata

            i = i + 1
        j = j + 1

    error = np.sqrt(error / sumobs) # Erro norma 2

    return error 

if __name__ == "__main__":
    global data, timestamps

    data = np.loadtxt(".local/parameter_adjustment_data.csv", delimiter=',')
    timestamps = data[:, 0]

    bounds = [ (1, 200), (0.01, 1), (1, 200) ]

    solution = scipy.optimize.differential_evolution(
        solve,
        bounds,
        strategy='best1bin',
        maxiter=5,
        popsize=4,
        atol=int(10**(-3)),
        tol=10**(-3),
        mutation=0.8,
        recombination=0.5,
        disp=True,
        # workers=4
    )

    best = solution.x
    error = solve(best)

    print(f"Best Solution: {best} {solution.success}")
    print(f"Error: {error}")

