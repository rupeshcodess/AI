import tkinter as tk
from tkinter import messagebox
import heapq

class Node:
    def __init__(self, position):
        self.position = position
        self.g = float('inf')  # Cost from start to node
        self.h = float('inf')  # Heuristic cost to goal
        self.f = float('inf')  # Total cost
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

ROW = 9
COL = 10
grid = [[1 for _ in range(COL)] for _ in range(ROW)]
src = None
goals = []

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(row, col):
    return grid[row][col] == 1

def calculate_h_value(node, goal):
    return abs(node.position[0] - goal[0]) + abs(node.position[1] - goal[1])

def ao_star_search(canvas):
    if not src or not goals:
        messagebox.showerror("Error", "Please set both source and at least one goal.")
        return

    open_list = []
    closed_list = set()
    start_node = Node(src)
    start_node.g = 0
    start_node.h = min(calculate_h_value(start_node, goal) for goal in goals)
    start_node.f = start_node.g + start_node.h

    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current_node = heapq.heappop(open_list)
        
        if any(current_node.position == goal for goal in goals):
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.reverse()
            for step in path:
                canvas.create_rectangle(step[1] * 40, step[0] * 40, step[1] * 40 + 40, step[0] * 40 + 40, fill='green')
            return

        closed_list.add(current_node.position)

        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
            if is_valid(new_pos[0], new_pos[1]) and is_unblocked(new_pos[0], new_pos[1]) and new_pos not in closed_list:
                neighbor_node = Node(new_pos)
                tentative_g = current_node.g + 1  # All edges have the same cost

                if tentative_g < neighbor_node.g:
                    neighbor_node.g = tentative_g
                    neighbor_node.h = min(calculate_h_value(neighbor_node, goal) for goal in goals)
                    neighbor_node.f = neighbor_node.g + neighbor_node.h
                    neighbor_node.parent = current_node
                    heapq.heappush(open_list, (neighbor_node.f, neighbor_node))

    messagebox.showinfo("Result", "Failed to find a path to any goal.")

def set_source(event):
    global src
    x, y = event.x // 40, event.y // 40
    if is_valid(y, x) and is_unblocked(y, x):
        src = (y, x)
        canvas.create_rectangle(x * 40, y * 40, x * 40 + 40, y * 40 + 40, fill='blue')

def set_goal(event):
    global goals
    x, y = event.x // 40, event.y // 40
    if is_valid(y, x) and is_unblocked(y, x):
        goals.append((y, x))
        canvas.create_rectangle(x * 40, y * 40, x * 40 + 40, y * 40 + 40, fill='red')

def toggle_block(event):
    x, y = event.x // 40, event.y // 40
    if is_valid(y, x):
        grid[y][x] = 0 if grid[y][x] == 1 else 1
        color = 'white' if grid[y][x] == 1 else 'black'
        canvas.create_rectangle(x * 40, y * 40, x * 40 + 40, y * 40 + 40, fill=color)

def start_pathfinding():
    canvas.delete("all")
    for row in range(ROW):
        for col in range(COL):
            color = 'white' if grid[row][col] == 1 else 'black'
            canvas.create_rectangle(col * 40, row * 40, col * 40 + 40, row * 40 + 40, fill=color)
    ao_star_search(canvas)

# GUI setup
root = tk.Tk()
root.title("Interactive AO* Pathfinding Algorithm")

canvas = tk.Canvas(root, width=COL * 40, height=ROW * 40)
canvas.pack()

canvas.bind("<Button-1>", set_source)  # Left click to set source
canvas.bind("<Button-3>", set_goal)  # Right click to set goals
canvas.bind("<Button-2>", toggle_block)  # Middle click to toggle block

start_button = tk.Button(root, text="Start Pathfinding", command=start_pathfinding)
start_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()
