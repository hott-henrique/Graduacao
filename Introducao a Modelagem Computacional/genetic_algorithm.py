import argparse

import numpy as np
import scipy

from odes import ode_sirs


class GeneticAlgorithm(object):

    def __init__(self, bounds: list[tuple], func, args):
        self.bounds = bounds
        self.n_genes = len(bounds)

        self.fitness_func = lambda individual: func(individual, *args)

    def evolution(self, P: int, G: int, mutation: float):
        assert mutation >= 0.0 and mutation <= 1.0

        population = self.generate_random_population(P)

        best_individual_of_each_generation = list()

        for g in range(G):
            population = self.crossover(population)

            self.mutate(population, probability=mutation)

            population, fitness_population = self.roulette_wheel_selection(population)

            i = np.argmin(fitness_population)

            best_individual_of_each_generation.append(np.copy(population[i]))

            print(f"Generation {g + 1}({np.mean(fitness_population)}): ({list(population[i])}, {fitness_population[i]})")

        best_individual_of_each_generation = np.array(best_individual_of_each_generation)

        fitness_best_individual_of_each_generation = np.apply_along_axis(
            func1d=self.fitness_func,
            axis=1,
            arr=best_individual_of_each_generation
        )

        best_individual = np.argmin(fitness_best_individual_of_each_generation)

        individual = best_individual_of_each_generation[best_individual]
        fitness = fitness_best_individual_of_each_generation[best_individual]


        return individual, fitness

    def generate_random_population(self, P: int):
        genes = np.array([ np.linspace(low, high, num=P) for low, high in self.bounds ])

        for gene in genes:
            np.random.shuffle(gene)

        population = genes.T

        return population

    def roulette_wheel_selection(self, population: np.ndarray):
        """
        Select P individuals with probabilty: 
            1 - (fitness(individual) / Summation(fitness(population)))
        Where fitness represents an error. So we aim to minimize it.
        """
        fitness_population = np.apply_along_axis(func1d=self.fitness_func, axis=1, arr=population)

        F = np.sum(fitness_population)

        new_population = list()
        fitness_new_population = list()

        i = 0
        while len(new_population) < len(population):
            individual, fitness = population[i], fitness_population[i]

            Pi = 1.0 - (fitness / F)

            if np.random.random() > Pi:
                continue

            new_population.append(individual)
            fitness_new_population.append(fitness)

            i = i + 1

            if i == len(population):
                i = 0

        new_population = np.array(new_population)
        fitness_new_population = np.array(fitness_new_population)

        return new_population, fitness_new_population

    def crossover(self, population: np.ndarray):
        P = len(population)

        new_population = np.ndarray(shape=population.shape)

        for i, j in zip(range(0, P, 2), range(1, P, 2)):
            M = population[i]
            F = population[j]

            pairing = np.random.randint(self.n_genes)

            new_population[i] = M
            new_population[i][:pairing] = F[:pairing]

            new_population[j] = F
            new_population[j][:pairing] = M[:pairing]

        return new_population

    def mutate(self, population: np.ndarray, probability: float):
        for individual in population:
            if np.random.random() > probability:
                continue

            g = np.random.randint(self.n_genes)

            individual[g] = np.random.uniform(*self.bounds[g])

# --------------------------------------------------------------------------------------

def simulate_sirs(ode_params, *simulation_params):
    ground_truth_data, steps, t_indices_pairing, initial_condition = simulation_params

    results = scipy.integrate.solve_ivp(
        fun=ode_sirs,
        args=ode_params,
        t_span=(0, np.max(steps)),
        y0=initial_condition,
        t_eval=steps,
        method="RK45"
    )

    S, I = results.y[[ 0, 1 ], :]

    errorS, errorI = 0, 0
    sumS, sumI = 0, 0

    for experimental_index, simulation_index in t_indices_pairing:
        truthS = ground_truth_data[experimental_index][1]
        truthI = ground_truth_data[experimental_index][2]

        errorS = errorS + np.float_power((S[simulation_index] - truthS), 2)
        errorI = errorI + np.float_power((I[simulation_index] - truthI), 2)

        sumS = sumS + truthS
        sumI = sumI + truthI

    error = np.sqrt(errorS / sumS) \
          + np.sqrt(errorI / sumI)

    return error

def get_pairing_indices(A: np.ndarray, B: np.ndarray, tolerance: float = np.power(1/10, 2)):
    pairing_indices = list()

    search_starting_point = 0

    for i, valueA in enumerate(A):
        for j in range(search_starting_point, len(B)):
            valueB = B[j]

            if np.abs(valueA - valueB) < tolerance:
                pairing_indices.append((i, j))
                search_starting_point = j + 1
                break

    pairing_indices = np.array(pairing_indices)

    return pairing_indices

def main(experimental_data_file_path: str):
    experimental_data = np.loadtxt(experimental_data_file_path, delimiter=',')

    tf, dt = 10, 0.01

    simulation_timestamps = np.arange(0, tf + dt, dt)

    simulation_params = (
        experimental_data,
        simulation_timestamps,
        get_pairing_indices(experimental_data[:, 0], simulation_timestamps, dt),
        np.array([ 995, 5, 0 ], dtype=np.float64)
    )

    ga = GeneticAlgorithm([ (0.01, 1), (0.01, 1), (0.01, 1) ], simulate_sirs, simulation_params)

    individual, error = ga.evolution(P=20, G=80, mutation=0.3)

    print(f"Best individual of evolution: {individual} | Fitness: {error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--experimental-data",
        help="Path to experimental data for SIRS ode model.",
        required=True
    )

    args = parser.parse_args()

    main(experimental_data_file_path=args.experimental_data)

