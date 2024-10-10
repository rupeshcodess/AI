import tkinter as tk
from tkinter import messagebox

class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        # Placeholder for future implementation
        pass

class BlockWorldGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Block World Game")

        self.agent = BlockWorldAgent()
        self.stacks = []
        self.goal_arrangement = []
        self.selected_block = None
        self.selected_stack_index = None
        self.dragged_block = None

        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack()

        self.initialize_game()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.solve_button = tk.Button(root, text="Check Goal", command=self.check_goal)
        self.solve_button.pack()

    def initialize_game(self):
        self.stacks = [["A", "B"], ["C"], ["D", "E"]]
        self.goal_arrangement = [["B", "A"], ["C"], ["D", "E"]]
        self.draw_stacks()

    def draw_stacks(self):
        self.canvas.delete("all")
        for index, stack in enumerate(self.stacks):
            x = index * 200 + 50
            for i, block in enumerate(stack):
                y = 300 - (i * 30)
                self.canvas.create_rectangle(x, y, x + 50, y + 30, fill="lightblue", outline="black")
                self.canvas.create_text(x + 25, y + 15, text=block)

        if self.dragged_block:
            self.canvas.create_rectangle(self.dragged_block[0] - 25, self.dragged_block[1] - 15,
                                          self.dragged_block[0] + 25, self.dragged_block[1] + 15,
                                          fill="yellow")
            self.canvas.create_text(self.dragged_block[0], self.dragged_block[1], text=self.selected_block)

    def on_click(self, event):
        for index, stack in enumerate(self.stacks):
            x = index * 200 + 50
            for i, block in enumerate(stack):
                y = 300 - (i * 30)
                if x <= event.x <= x + 50 and y <= event.y <= y + 30:
                    self.selected_block = block
                    self.selected_stack_index = index
                    self.dragged_block = (event.x, event.y)  # Initialize drag position
                    self.draw_stacks()
                    return

    def on_drag(self, event):
        if self.selected_block:
            self.dragged_block = (event.x, event.y)
            self.draw_stacks()

    def on_release(self, event):
        if self.selected_block:
            for index in range(len(self.stacks)):
                x = index * 200 + 50
                if x <= event.x <= x + 50:
                    if index != self.selected_stack_index:
                        # Move block to new stack
                        self.stacks[index].append(self.selected_block)
                        self.stacks[self.selected_stack_index].remove(self.selected_block)  # Remove from old stack
                    break
            self.selected_block = None
            self.selected_stack_index = None
            self.dragged_block = None  # Reset drag
            self.draw_stacks()

    def check_goal(self):
        current_arrangement = [stack[:] for stack in self.stacks]
        if current_arrangement == self.goal_arrangement:
            messagebox.showinfo("Goal Achieved!", "Congratulations, you reached the goal!")
        else:
            messagebox.showwarning("Not Yet!", "Keep trying to reach the goal.")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlockWorldGame(root)
    root.mainloop()
