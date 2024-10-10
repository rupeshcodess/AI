import tkinter as tk
from tkinter import messagebox

# Initial Sudoku puzzle
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 0, 0]
]

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.solution = None

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint_var in self.constraints[var]:
            if constraint_var in assignment and assignment[constraint_var] == value:
                return False
        return True

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.grid_entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_input_grid()
        self.solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku)
        self.solve_button.grid(row=9, column=0, columnspan=9, pady=10)  # Use grid for the button

    def create_input_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 24), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.grid_entries[i][j] = entry
                if puzzle[i][j] != 0:
                    entry.insert(0, str(puzzle[i][j]))
                    entry.config(state='readonly', disabledforeground='black')

    def get_puzzle_from_entries(self):
        return [[int(entry.get()) if entry.get() else 0 for entry in row] for row in self.grid_entries]

    def solve_sudoku(self):
        puzzle = self.get_puzzle_from_entries()
        
        # Set up CSP
        variables = [(i, j) for i in range(9) for j in range(9)]
        domains = {var: set(range(1, 10)) if puzzle[var[0]][var[1]] == 0 else {puzzle[var[0]][var[1]]} for var in variables}

        # Add constraints
        constraints = {}
        for i in range(9):
            for j in range(9):
                self.add_constraint((i, j), constraints)

        csp = CSP(variables, domains, constraints)
        sol = csp.solve()

        if sol is None:
            messagebox.showinfo("Result", "No solution exists.")
            return

        # Update the GUI with the solution
        for (i, j), value in sol.items():
            self.grid_entries[i][j].config(state='normal')
            self.grid_entries[i][j].delete(0, tk.END)
            self.grid_entries[i][j].insert(0, str(value))
            self.grid_entries[i][j].config(state='readonly', disabledforeground='black')

    def add_constraint(self, var, constraints):
        constraints[var] = []
        for i in range(9):
            if i != var[0]:
                constraints[var].append((i, var[1]))
            if i != var[1]:
                constraints[var].append((var[0], i))
        sub_i, sub_j = var[0] // 3, var[1] // 3
        for i in range(sub_i * 3, (sub_i + 1) * 3):
            for j in range(sub_j * 3, (sub_j + 1) * 3):
                if (i, j) != var:
                    constraints[var].append((i, j))

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
