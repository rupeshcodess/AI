import tkinter as tk
from tkinter import messagebox
from collections import deque

class GraphVisualization(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.title("Breadth First Search Visualization")
        self.geometry("800x600")

        # Main frame setup
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas frame
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas setup
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Control frame
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(pady=10)

        # Instructions label
        self.instruction_label = tk.Label(self.control_frame, text="Enter the goal node and click 'Start BFS'.", font=("Arial", 12))
        self.instruction_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Goal node input
        self.goal_label = tk.Label(self.control_frame, text="Goal Node:", font=("Arial", 12))
        self.goal_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.goal_entry = tk.Entry(self.control_frame, font=("Arial", 12))
        self.goal_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button = tk.Button(self.control_frame, text="Start BFS", font=("Arial", 12), command=self.start_bfs)
        self.start_button.grid(row=1, column=2, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")
        self.status_bar = tk.Label(self.main_frame, textvariable=self.status_var, anchor=tk.W, relief=tk.SUNKEN, height=1, font=("Arial", 10))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Initialize graph-related variables
        self.graph = graph
        self.node_positions = {}
        self.visited = set()
        self.paths = []  
        self.goal_node = None

        self.setup_graph()

    def setup_graph(self):
        # Node positions
        self.node_positions = {
            'A': (100, 100),
            'B': (300, 100),
            'C': (500, 100),
            'D': (300, 300),
            'E': (500, 300)
        }

        # Draw nodes
        for node, position in self.node_positions.items():
            x, y = position
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue", tags=node)
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_positions[node]
            for neighbor in neighbors:
                x2, y2 = self.node_positions[neighbor]
                if x1 < x2 or y1 < y2:  # Prevent drawing duplicate edges
                    self.canvas.create_line(x1, y1, x2, y2, tags=f"{node}-{neighbor}")

    def start_bfs(self):
        self.goal_node = self.goal_entry.get().strip().upper()
        if self.goal_node not in self.graph:
            messagebox.showerror("Error", f"Goal node '{self.goal_node}' not found in graph!")
            return

        self.visited.clear()
        self.paths.clear()
        self.canvas.delete("highlight")
        self.status_var.set(f"Status: Starting BFS from 'A' to '{self.goal_node}'")
        self.bfs('A')  # Start BFS from node 'A'

        if not self.paths:
            messagebox.showinfo("Result", f"No path found to goal node '{self.goal_node}'")
        else:
            paths_str = "\n".join([" -> ".join(path) for path in self.paths])
            messagebox.showinfo("Result", f"Paths to goal node '{self.goal_node}':\n{paths_str}")

        self.status_var.set(f"Status: BFS complete")

    def bfs(self, start_node):
        queue = deque([(start_node, [start_node])])
        self.visited.add(start_node)
        x, y = self.node_positions[start_node]
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightgreen", tags="highlight")
        self.update()
        self.after(500)

        while queue:
            node, path = queue.popleft()
            if node == self.goal_node:
                self.paths.append(path)
                continue

            for neighbor in self.graph[node]:
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]
                    self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="highlight")
                    self.update()
                    self.after(500)
                    x, y = self.node_positions[neighbor]
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightgreen", tags="highlight")
                    self.update()
                    self.after(500)

if __name__ == "__main__":
    graph = {
        'A': ['B'],
        'B': ['A', 'C', 'D'],
        'C': ['B', 'E'],
        'D': ['B'],
        'E': ['C']
    }

    app = GraphVisualization(graph)
    app.mainloop()
