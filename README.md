# Travelling Salesman Problem Algorithms

Welcome to the Travelling Salesman Problem Algorithms repository! This collection includes implementations of five different algorithms to solve the Travelling Salesman Problem (TSP). The TSP is a classic optimization problem where the goal is to find the shortest possible route that visits a given set of cities and returns to the original city.

## Algorithms Included:

1. **Nearest Neighbor Algorithm**

   This algorithm starts from a randomly selected city and selects the nearest unvisited city at each step until all cities are visited. The route is then closed by returning to the starting city.

2. **Hill Climbing Algorithm**

   This local search algorithm iteratively makes small adjustments to the current solution, accepting the changes if they lead to an improvement. It continues until no further improvements can be made.

3. **Genetic Algorithm**

   The Genetic Algorithm involves evolving a population of candidate solutions using genetic operators such as crossover and mutation. It aims to reach an optimal solution through natural selection.

4. **Simulated Annealing**

   Simulated Annealing is a probabilistic optimization algorithm inspired by annealing in metallurgy. It accepts worse solutions with a decreasing probability to escape local optima.

5. **Tabu Search**

   Tabu Search uses a memory-based approach to avoid revisiting recently explored solutions. It maintains a list of forbidden (tabu) moves to guide the search towards unexplored regions.

## Getting Started

To explore and use these algorithms, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/tsp-algorithms.git`
2. Navigate to the project directory: `cd tsp-algorithms`
3. Check each algorithm's implementation for specific usage instructions.
