import pandas as pd
import math

# Loading data from Excel
distance_matrix = pd.read_excel("Data_TSP_48.xlsx", index_col=0) # Data_TSP_76.xlsx, Data_TSP_127.xlsx

def nearest_neighbor(distances, start_city):
    num_cities = len(distance_matrix)
    visited = [False] * num_cities
    tour = []
    total_distance = 0
    
    # Choosing the starting city
    current_city = start_city
    tour.append(current_city)
    visited[current_city] = True
    
    # The loop continues until all cities are visited
    while len(tour) < num_cities:
        nearest_city = None
        nearest_distance = math.inf

        # Finding the nearest unvisited neighbor 
        for city in range(num_cities):
            if not visited[city]:
                distance = distances.iloc[current_city, city]
                if distance < nearest_distance:
                    nearest_city = city
                    nearest_distance = distance

        # Moving to the nearest neighbor and calculating the distance
        current_city = nearest_city
        tour.append(current_city)
        visited[current_city] = True
        total_distance += nearest_distance

    # Returning to the starting city
    tour.append(start_city)
    total_distance += distances.iloc[current_city, start_city]

    return tour, total_distance

# Variables to track the best result
best_tour = None
best_total_distance = math.inf

# Testing the algorithm for each city as the starting city
for start_city in range(len(distance_matrix)):
    tour, total_distance = nearest_neighbor(distance_matrix, start_city)
    
    if total_distance < best_total_distance:
        best_tour = tour
        best_total_distance = total_distance

print(f"Best tour: {best_tour}")
print(f"Total distance: {best_total_distance}")