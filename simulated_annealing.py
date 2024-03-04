from simanneal import Annealer
import random
import pandas as pd

class TSPProblem(Annealer):
    def __init__(self, state, distance_matrix):
        super(TSPProblem, self).__init__(state)
        self.distance_matrix = distance_matrix

    def move(self):
        change_type = random.choice(['swap', 'insert', 'invert'])
        
        if change_type == 'swap':
            self.swap()
        elif change_type == 'insert':
            self.insert()
        elif change_type == 'invert':
            self.invert()

    def swap(self):
        index1, index2 = random.sample(range(len(self.state)), 2)
        self.state[index1], self.state[index2] = self.state[index2], self.state[index1]

    def insert(self):
        city = random.choice(self.state)
        index = random.randint(0, len(self.state) - 1)
        self.state.remove(city)
        self.state.insert(index, city)

    def invert(self):
        start, end = sorted(random.sample(range(len(self.state)), 2))
        self.state[start:end+1] = reversed(self.state[start:end+1])

    def energy(self):
        total_distance = 0
        for i in range(len(self.state) - 1):
            total_distance += self.distance_matrix[self.state[i] - 1][self.state[i + 1] - 1]
        total_distance += self.distance_matrix[self.state[-1] - 1][self.state[0] - 1]
        return total_distance

    @staticmethod
    def run_with_parameters(excel_path, Tmax, Tmin, steps, method, num_runs):
        df = pd.read_excel(excel_path, index_col=0)
        initial_solution = list(range(1, len(df) + 1))
        
        best_overall_energy = float('inf') 
        total_energy = 0

        for _ in range(num_runs):
            tsp_problem = TSPProblem(initial_solution, df.values.tolist())
            tsp_problem.Tmax = Tmax
            tsp_problem.Tmin = Tmin
            tsp_problem.steps = steps

            if method == 'swap':
                tsp_problem.move = tsp_problem.swap
            elif method == 'insert':
                tsp_problem.move = tsp_problem.insert
            elif method == 'invert':
                tsp_problem.move = tsp_problem.invert
            else:
                raise ValueError(f"Unknown neighborhood method: {method}")

            best_solution, best_energy = tsp_problem.anneal()

            if best_energy < best_overall_energy:
                best_overall_energy = best_energy

            total_energy += best_energy

        average_energy = total_energy / num_runs

        return {
            'Max Temp': Tmax,
            'Min Temp': Tmin,
            'Steps': steps,
            'Method': method,
            'Best Energy': best_overall_energy,
            'Average Energy': average_energy
        }

excel_file_path = "Data_TSP_48.xlsx"

Tmax_values = [10, 10, 10, 20]
Tmin_values = [1, 0.5, 10, 5]
steps_values = [10, 50, 10, 10]

neighbor_methods = ['swap', 'insert', 'invert']
results = []

for Tmax in Tmax_values:
    for Tmin in Tmin_values:
        for steps in steps_values:
            for method in neighbor_methods:
                result = TSPProblem.run_with_parameters(excel_file_path, Tmax, Tmin, steps, method, 20)
                results.append(result)

results_df = pd.DataFrame(results)
results_df.to_excel('annealing_results_48.xlsx', index=False)