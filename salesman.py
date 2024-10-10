import tkinter as tk
from tkinter import messagebox
import numpy as np

class TravelingSalesman:
    def __init__(self, cost_matrix):
        self.n = len(cost_matrix)
        self.cost_matrix = cost_matrix
        self.visited = np.zeros(self.n, dtype=int)
        self.cost = 0
        self.path = []

    def solve(self, current_city):
        self.visited[current_city] = 1
        self.path.append(current_city + 1)  # Store the path in 1-based index
        adj_vertex = -1
        min_val = float('inf')

        for k in range(self.n):
            if self.cost_matrix[current_city][k] != 0 and self.visited[k] == 0:
                if self.cost_matrix[current_city][k] < min_val:
                    min_val = self.cost_matrix[current_city][k]
                    adj_vertex = k

        if min_val != float('inf'):
            self.cost += min_val

        if adj_vertex == -1:
            adj_vertex = 0  # Return to the starting city
            self.path.append(adj_vertex + 1)  # Include starting city in the path
            self.cost += self.cost_matrix[current_city][adj_vertex]
            return

        self.solve(adj_vertex)

class TSPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traveling Salesman Problem Solver (3x3)")
        self.root.geometry("400x400")  # Set window size

        self.entries = []
        self.create_widgets()

        self.solve_button = tk.Button(root, text="Solve TSP", command=self.solve_tsp, height=2, width=15)
        self.solve_button.grid(row=4, column=0, columnspan=3)

    def create_widgets(self):
        tk.Label(self.root, text="Enter the cost matrix (3x3):", font=("Arial", 12)).grid(row=0, column=0, columnspan=3)

        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = tk.Entry(self.root, width=5, font=("Arial", 14))
                entry.grid(row=i + 1, column=j)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def solve_tsp(self):
        cost_matrix = []

        try:
            for i in range(3):
                row = []
                for j in range(3):
                    value = self.entries[i][j].get()
                    row.append(int(value) if value else 0)
                cost_matrix.append(row)

            tsp_solver = TravelingSalesman(cost_matrix)
            tsp_solver.solve(0)

            path = " -> ".join(map(str, tsp_solver.path))
            messagebox.showinfo("Solution", f"Shortest Path: {path}\nMinimum Cost: {tsp_solver.cost}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers in the cost matrix.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPGUI(root)
    root.mainloop()
