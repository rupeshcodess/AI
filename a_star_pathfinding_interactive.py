import math
import heapq
import tkinter as tk
from tkinter import messagebox

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

# Define the grid size
ROW = 9
COL = 10

# Global variables to store grid, source, and destination
grid = [[1 for _ in range(COL)] for _ in range(ROW)]
src = None
dest = None

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(row, col):
    return grid[row][col] == 1

def is_destination(row, col):
    return (row, col) == dest

def calculate_h_value(row, col):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

def trace_path(cell_details):
    path = []
    row, col = dest

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row, col = temp_row, temp_col

    path.append((row, col))
    path.reverse()
    return path

def a_star_search(canvas):
    if not src or not dest:
        messagebox.showerror("Error", "Please set both source and destination.")
        return

    if not is_unblocked(src[0], src[1]) or not is_unblocked(dest[0], dest[1]):
        messagebox.showerror("Error", "Source or destination is blocked.")
        return

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    found_dest = False

    while open_list:
        p = heapq.heappop(open_list)
        i, j = p[1], p[2]
        closed_list[i][j] = True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]

            if is_valid(new_i, new_j) and is_unblocked(new_i, new_j) and not closed_list[new_i][new_j]:
                if is_destination(new_i, new_j):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    found_dest = True
                    path = trace_path(cell_details)

                    for step in path:
                        canvas.create_rectangle(step[1] * 40, step[0] * 40, step[1] * 40 + 40, step[0] * 40 + 40, fill='green')
                    canvas.create_rectangle(dest[1] * 40, dest[0] * 40, dest[1] * 40 + 40, dest[0] * 40 + 40, fill='red')
                    return

                g_new = cell_details[i][j].g + 1.0
                h_new = calculate_h_value(new_i, new_j)
                f_new = g_new + h_new

                if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                    heapq.heappush(open_list, (f_new, new_i, new_j))
                    cell_details[new_i][new_j].f = f_new
                    cell_details[new_i][new_j].g = g_new
                    cell_details[new_i][new_j].h = h_new
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j

    if not found_dest:
        messagebox.showinfo("Result", "Failed to find the destination cell.")

def set_source(event):
    global src
    x, y = event.x // 40, event.y // 40
    if is_valid(y, x) and is_unblocked(y, x):
        src = (y, x)
        canvas.create_rectangle(x * 40, y * 40, x * 40 + 40, y * 40 + 40, fill='blue')

def set_destination(event):
    global dest
    x, y = event.x // 40, event.y // 40
    if is_valid(y, x) and is_unblocked(y, x):
        dest = (y, x)
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
    a_star_search(canvas)

# GUI setup
root = tk.Tk()
root.title("Interactive A* Pathfinding Algorithm")

canvas = tk.Canvas(root, width=COL * 40, height=ROW * 40)
canvas.pack()

canvas.bind("<Button-1>", set_source)  # Left click to set source
canvas.bind("<Button-3>", set_destination)  # Right click to set destination
canvas.bind("<Button-2>", toggle_block)  # Middle click to toggle block

start_button = tk.Button(root, text="Start Pathfinding", command=start_pathfinding)
start_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()
