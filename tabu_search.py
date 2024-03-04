import numpy as np
import pandas as pd
import random
import time
from tqdm import tqdm

# Function to load distance matrix from an Excel file
def load_distance_matrix(file_path):
    distance_matrix_df = pd.read_excel(file_path, index_col=0)
    distance_matrix = distance_matrix_df.to_numpy(dtype=float)
    return distance_matrix

# Function to generate a random initial solution
def random_solution(distance_matrix):
    cities = list(range(len(distance_matrix)))
    random_route = np.array(random.sample(cities, len(cities)))
    return random_route

# Function to calculate the distance of a route
def calc_distance(distance_matrix, route):
    route_array = np.array(route)
    total_distance = 0
    for i in range(len(route_array) - 1):
        current_city = route_array[i]
        next_city = route_array[i + 1]
        total_distance += distance_matrix[current_city, next_city]
    total_distance += distance_matrix[route_array[-1], route_array[0]]  # add distance from the last city to the first
    return total_distance

# Swap method for finding a neighbor (randomly swap two cities)
def swap(solution):
    neighbors = []
    for _ in range(len(solution)):
        random_indices = random.sample(range(len(solution)), 2)
        neighbor = solution.copy()
        neighbor[random_indices[0]] = solution[random_indices[1]]
        neighbor[random_indices[1]] = solution[random_indices[0]]
        neighbors.append(neighbor)
    return neighbors

# Insert method for finding a neighbor (randomly choose one city and place it in a random position)
def insert(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbors = []
        for i in range(len(solution)):
            new_route = solution.copy()
            city_to_place = random.choice(new_route)
            new_route = np.delete(new_route, np.where(new_route == city_to_place))
            random_position = random.randint(0, len(new_route))
            neighbor = np.insert(new_route, random_position, city_to_place)
            neighbors.append(neighbor)

    return neighbors

# Reverse method for finding a neighbor (randomly choose two cities and reverse the order of cities between them, inclusive)
def reverse(solution):
    neighbors = []
    for i in range(len(solution)):
        new_route = solution.copy()
        start_idx = random.randint(0, len(solution) - 2)
        end_idx = random.randint(start_idx + 1, len(solution) - 1)
        reversed_subroute = list(reversed(new_route[start_idx:end_idx + 1]))
        new_route[start_idx:end_idx + 1] = reversed_subroute
        neighbor = new_route
        neighbors.append(neighbor)

    return neighbors

# Main function 
def tabu_search(initial_solution, max_iterations, tabu_list_size, distance_matrix, neighbor_function):
    best_solution = initial_solution
    current_solution = initial_solution
    tabu_list = []

    for _ in tqdm(range(max_iterations)):
        neighbors = neighbor_function(current_solution)
        best_neighbor = None
        best_neighbor_fitness = float('inf')

        for neighbor in neighbors:
            if not any(np.array_equal(neighbor, tabu_item) for tabu_item in tabu_list):
                neighbor_fitness = calc_distance(distance_matrix, neighbor)
                if neighbor_fitness < best_neighbor_fitness:
                    best_neighbor = neighbor
                    best_neighbor_fitness = neighbor_fitness

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        if calc_distance(distance_matrix, best_neighbor) < calc_distance(distance_matrix, best_solution):
            best_solution = best_neighbor

    return best_solution

# Run calculations for all combinations from the selected parameter lists
def run_algorithm_combinations(file_path):
    distance_matrix = load_distance_matrix(file_path)
    cities = list(range(len(distance_matrix)))
    results = []

    # Define combinations of parameters
    max_iterations_values = [100, 200, 400, 500]
    tabu_list_size_values = [5, 10, 20, 30]
    neighbor_functions = [swap, insert, reverse]

    for max_iterations in max_iterations_values:
        for tabu_list_size in tabu_list_size_values:
            for neighbor_function in neighbor_functions:
                total_fitness = 0
                best_fitness = float('inf')
                best_route = None

                for _ in range(10):
                    initial_solution = random_solution(distance_matrix)
                    best_solution = tabu_search(initial_solution, max_iterations, tabu_list_size, distance_matrix, neighbor_function)

                    current_fitness = calc_distance(distance_matrix, best_solution)
                    total_fitness += current_fitness

                    if current_fitness < best_fitness:
                        best_fitness = current_fitness
                        best_route = best_solution

                average_fitness = total_fitness / 10
                results.append({
                    'Max Iterations': max_iterations,
                    'Tabu List Size': tabu_list_size,
                    'Neighbor Function': neighbor_function.__name__,
                    'Average Fitness': average_fitness,
                    'Best Fitness': best_fitness,
                    'Best Route': best_route.tolist()
                })

    results_df = pd.DataFrame(results)
    results_df.to_excel('tabu_search_results_127.xlsx', index=False)

# Usage
file_path = 'Data_TSP_48.xlsx'
run_algorithm_combinations(file_path)