import random
import tkinter as tk
from tkinter import messagebox

# Distance matrix representing distances between cities
distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# City names for display purposes
city_names = ["City 1", "City 2", "City 3", "City 4"]

def total_distance(path):
    total = 0
    for i in range(len(path) - 1):
        total += distance_matrix[path[i]][path[i + 1]]
    total += distance_matrix[path[-1]][path[0]]  # Return to starting city
    return total

def hill_climbing_tsp(num_cities, max_iterations=10000):
    current_path = list(range(num_cities))
    current_distance = total_distance(current_path)

    for _ in range(max_iterations):
        neighbor_path = current_path.copy()
        i, j = random.sample(range(num_cities), 2)
        neighbor_path[i], neighbor_path[j] = neighbor_path[j], neighbor_path[i]
        neighbor_distance = total_distance(neighbor_path)

        if neighbor_distance < current_distance:
            current_path = neighbor_path
            current_distance = neighbor_distance
            
    return current_path

def draw_path(path):
    canvas.delete("all")
    width, height = 400, 400
    city_positions = [(100, 100), (300, 100), (100, 300), (300, 300)]  # Sample positions
    for i, pos in enumerate(city_positions):
        canvas.create_oval(pos[0]-20, pos[1]-20, pos[0]+20, pos[1]+20, fill='blue')
        canvas.create_text(pos[0], pos[1], text=city_names[i], fill='white')

    for i in range(len(path)):
        start = city_positions[path[i]]
        end = city_positions[path[(i + 1) % len(path)]]
        canvas.create_line(start[0], start[1], end[0], end[1], fill='red', width=2)

def run_tsp():
    num_cities = len(distance_matrix)
    solution = hill_climbing_tsp(num_cities)
    draw_path(solution)
    optimal_distance = total_distance(solution)
    path_str = " -> ".join(city_names[i] for i in solution)
    
    messagebox.showinfo("TSP Result", f"Optimal path: {path_str}\nTotal distance: {optimal_distance}")

# GUI setup
root = tk.Tk()
root.title("Hill Climbing TSP Game")

frame = tk.Frame(root)
frame.pack(pady=20)

canvas = tk.Canvas(frame, width=400, height=400, bg='lightgrey')
canvas.pack()

run_button = tk.Button(root, text="Run Hill Climbing TSP", command=run_tsp)
run_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=5)

root.mainloop()
