import tkinter as tk
from tkinter import messagebox
import random

class NumberPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Puzzle Game")

        self.size = 3
        self.empty_tile = (self.size - 1, self.size - 1)
        self.board = self.create_solvable_puzzle()
        self.buttons = {}
        self.create_ui()

    def create_solvable_puzzle(self):
        """Create a simple solvable puzzle by starting with an ordered board and performing a few swaps"""
        numbers = list(range(self.size * self.size))
        board = [numbers[i * self.size:(i + 1) * self.size] for i in range(self.size)]
        
        # Perform a few moves to shuffle
        for _ in range(10):
            self.shuffle_board(board)
        
        return board

    def shuffle_board(self, board):
        """Shuffle the board by making random moves"""
        empty_i, empty_j = self.empty_tile
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        valid_moves = []
        
        for di, dj in directions:
            ni, nj = empty_i + di, empty_j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                valid_moves.append((ni, nj))
        
        if valid_moves:
            ni, nj = random.choice(valid_moves)
            board[empty_i][empty_j], board[ni][nj] = board[ni][nj], board[empty_i][empty_j]
            self.empty_tile = (ni, nj)

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.frame.grid_rowconfigure(tuple(range(self.size)), weight=1)
        self.frame.grid_columnconfigure(tuple(range(self.size)), weight=1)
        
        self.update_ui()

    def update_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        button_size = 4

        for i in range(self.size):
            for j in range(self.size):
                tile_value = self.board[i][j]
                if tile_value != 0:
                    button = tk.Button(self.frame, text=str(tile_value), width=button_size, height=button_size,
                                       command=lambda i=i, j=j: self.move_tile(i, j))
                    button.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                    self.buttons[(i, j)] = button
                else:
                    self.empty_tile = (i, j)

    def move_tile(self, i, j):
        """Move the tile at (i, j) if possible"""
        empty_i, empty_j = self.empty_tile

        if (abs(empty_i - i) == 1 and empty_j == j) or (abs(empty_j - j) == 1 and empty_i == i):
            self.board[empty_i][empty_j], self.board[i][j] = self.board[i][j], self.board[empty_i][empty_j]
            self.empty_tile = (i, j)
            self.update_ui()
            if self.is_solved():
                messagebox.showinfo("Puzzle Solved", "Congratulations! You have solved the puzzle.")

    def is_solved(self):
        """Check if the puzzle is solved"""
        expected = list(range(1, self.size * self.size)) + [0]
        current = [self.board[i][j] for i in range(self.size) for j in range(self.size)]
        return expected == current

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")   
    app = NumberPuzzle(root)
    root.mainloop()
