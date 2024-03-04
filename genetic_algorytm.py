import random
import pandas as pd
from deap import base, creator, tools, algorithms
import itertools
from tqdm import tqdm 

# Load data from Excel file
df = pd.read_excel("Data_TSP_76.xlsx", index_col=0)
data = df.values.tolist()

# DEAP creator definitions
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# DEAP toolbox initialization
toolbox = base.Toolbox()

# Register tools
toolbox.register("indices", random.sample, range(len(data)), len(data))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    distance = sum(data[individual[i]][individual[i + 1]] for i in range(len(individual) - 1))
    distance += data[individual[-1]][individual[0]]
    return distance,

toolbox.register("evaluate", evaluate)

def test_combinations(data, num_repetitions=5):
    selection_methods = [tools.selTournament, tools.selRoulette]
    crossover_methods = [tools.cxOrdered, tools.cxPartialyMatched]
    population_sizes = [50, 100, 200, 500]
    num_generations = [1000, 1500, 2000, 3000]
    mutpb_values = [0.05, 0.1, 0.2, 0.3]

    all_combinations = list(itertools.product(selection_methods, crossover_methods, population_sizes, num_generations, mutpb_values))

    results = []

    for selection, crossover, pop_size, num_gen, mutpb in (all_combinations):
        best_score = float('inf')
        best_individual = None
        total_result = 0

        for _ in tqdm(range(num_repetitions)):
            if selection == tools.selTournament:
                toolbox.register("select", selection, tournsize=6)
            else:
                toolbox.register("select", selection)
            
            toolbox.register("mate", crossover)
            toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutpb)

            population = toolbox.population(n=pop_size)

            algorithms.eaMuPlusLambda(population, toolbox, mu=pop_size, lambda_=2*pop_size, cxpb=0.7, mutpb=mutpb, ngen=num_gen, stats=None, halloffame=None)

            best_individual_current = tools.selBest(population, k=1)[0]
            best_score_current = evaluate(best_individual_current)[0]
            
            if best_score_current < best_score:
                best_score = best_score_current
                best_individual = best_individual_current

            total_result += best_score_current

        average_score = total_result / 5

        results.append({
            'Best Route': best_individual,
            'Selection Method': selection.__name__,
            'Crossover Method': crossover.__name__,
            'Population Size': pop_size,
            'Number of Generations': num_gen,
            'Mutation Probability (mutpb)': mutpb,
            'Best Distance': best_score,
            'Average Distance': average_score
            })

    df_results = pd.DataFrame(results)
    df_results.to_excel("genetic_result_76_Second_Version.xlsx")

# Run the function testing different combinations
test_combinations(data)