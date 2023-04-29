import numpy as np


class GeneticAlgorithm(object):

    def __init__(self, bounds: list[tuple], func, args, **kwargs):
        self.bounds = bounds
        self.n_genes = len(bounds)

        self.fitness_as_error = kwargs.get("fitness_as_error", False)

        factor = 1 if not self.fitness_as_error else -1

        self.fitness_func = lambda individual: factor * func(individual, *args)

    def evolution(self, P: int, G: int, mutation: float):
        assert mutation >= 0.0 and mutation <= 1.0

        population = self.generate_random_population(P)

        best_fitness = np.inf if self.fitness_as_error else 0

        for g in range(G):
            fitness_population = np.apply_along_axis(
                func1d=self.fitness_func,
                axis=1,
                arr=population
            )

            i = np.argmax(fitness_population)

            individual = np.copy(population[i])
            best_fitness = fitness_population[i]

            population = self.crossover(population)

            self.mutate(population, probability=mutation)

            population = self.roulette_wheel_selection(population, fitness_population)

            population[0] = individual

            print(f"Generation {g + 1}: f(x)= {np.abs(best_fitness)}")

        print("Finished executing Genetic Algorithm.")

        return population[0], best_fitness

    def generate_random_population(self, P: int):
        genes = np.array([ np.linspace(low, high, num=P) for low, high in self.bounds ])

        for gene in genes:
            np.random.shuffle(gene)

        population = genes.T

        return population

    def roulette_wheel_selection(self, population: np.ndarray, fitness_population: np.ndarray):
        F = np.sum(fitness_population)

        new_population = list()

        p = lambda fitness: (fitness / F)

        if self.fitness_as_error:
            p = lambda fitness: 1 - (fitness / F)

        i = 0
        while len(new_population) < len(population):
            individual, fitness = population[i], fitness_population[i]

            if np.random.random() > p(fitness):
                continue

            new_population.append(individual)

            i = i + 1

            if i == len(population):
                i = 0

        new_population = np.array(new_population)

        return new_population

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

