import numpy as np
import pandas as pd
import random
from tqdm import tqdm

# import data
def load_distance_matrix(file_path):
    distance_matrix_df = pd.read_excel(file_path, index_col=0)
    distance_matrix = distance_matrix_df.to_numpy(dtype=float)
    return distance_matrix

# creating a random route
def random_solution(distance_matrix):
    cities = list(range(len(distance_matrix)))
    random_route = np.array(random.sample(cities, len(cities)))
    return random_route

# calculating route distance 
def calculate_route_distance(distance_matrix, route):
    route_array = np.array(route)
    total_distance = 0
    for i in range(len(route_array) - 1):
        current_city = route_array[i]
        next_city = route_array[i + 1]
        total_distance += distance_matrix[current_city, next_city]
    total_distance += distance_matrix[route_array[-1], route_array[0]]  # adding distance from the last city to the first
    return total_distance

# swap method for finding a neighbor (randomly swap two cities)
def swap(distance_matrix, cities):
    random_indices = random.sample(range(len(cities)), 2)
    neighbor = cities.copy()
    neighbor[random_indices[0]] = cities[random_indices[1]]
    neighbor[random_indices[1]] = cities[random_indices[0]]

    return neighbor, calculate_route_distance(distance_matrix, neighbor)

# insert method for finding a neighbor (randomly choose a city and place it in a random position)
def insert(distance_matrix, cities):
    new_route = cities.copy()
    city_to_place = random.choice(new_route)
    new_route = np.delete(new_route, np.where(new_route == city_to_place))
    random_position = random.randint(0, len(new_route))
    neighbor = np.insert(new_route, random_position, city_to_place)
    
    return neighbor, calculate_route_distance(distance_matrix, neighbor)

# reverse method for finding a neighbor (randomly choose two cities and reverse the order of cities between them, inclusive)
def reverse(distance_matrix, cities):
    new_route = cities.copy()
    start_idx = random.randint(0, len(cities) - 2)  # choose starting index from 0 to the second-to-last city
    end_idx = random.randint(start_idx + 1, len(cities) - 1)  # choose ending index greater than the starting index
    reversed_subroute = list(reversed(new_route[start_idx:end_idx + 1]))
    new_route[start_idx:end_idx + 1] = reversed_subroute
    neighbor = new_route
    
    return neighbor, calculate_route_distance(distance_matrix, neighbor)

# main method
def hill_climbing_multistart(distance_matrix, max_iterations, max_iterations_without_improvement, num_restarts, neighbor_function):
    best_solution = None
    best_distance = float('inf')

    for restart in tqdm(range(1, num_restarts + 1)):
        # initialize a random solution
        current_solution = random_solution(distance_matrix)
        current_distance = calculate_route_distance(distance_matrix, current_solution)

        iterations_without_improvement = 0

        for iteration in range(1, max_iterations + 1):
            # generate neighbors
            neighbor, neighbor_distance = neighbor_function(distance_matrix, current_solution)

            # check if the neighbor solution is better
            if neighbor_distance < current_distance:
                current_solution = neighbor
                current_distance = neighbor_distance
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

            # check if the iteration limit without improvement is reached
            if iterations_without_improvement >= max_iterations_without_improvement:
                break

        # update the best solution
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance

    return best_solution, best_distance

def run_algorithm_combinations(file_path):
    distance_matrix = load_distance_matrix(file_path)
    cities = list(range(len(distance_matrix)))
    results = []

    # parameter combinations
    max_iterations_values = [1000, 2000, 5000, 10000]
    max_iterations_without_improvement_values = [100, 200, 500, 1000]
    neighbor_functions = [swap, insert, reverse]

    for max_iterations in max_iterations_values:
        for max_iterations_without_improvement in max_iterations_without_improvement_values:
            for neighbor_function in neighbor_functions:
                total_fitness = 0
                best_fitness = float('inf')
                best_route = None

                for _ in range(10):  
                    best_solution, current_fitness = hill_climbing_multistart(
                        distance_matrix,
                        max_iterations,
                        max_iterations_without_improvement,
                        20,  
                        neighbor_function
                    )

                    total_fitness += current_fitness

                    if current_fitness < best_fitness:
                        best_fitness = current_fitness
                        best_route = best_solution

                average_fitness = total_fitness / 10
                results.append({
                    'Max Iterations': max_iterations,
                    'Max Iterations Without Improvement': max_iterations_without_improvement,
                    'Neighbor Function': neighbor_function.__name__,
                    'Average Fitness': average_fitness,
                    'Best Fitness': best_fitness,
                    'Best Route': best_route.tolist()
                })

    results_df = pd.DataFrame(results)
    results_df.to_excel('hill_climbing_multistart_results_127.xlsx', index=False)

file_path = 'Data_TSP_127.xlsx'
run_algorithm_combinations(file_path)