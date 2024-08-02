import tkinter as tk
from tkinter import messagebox

class NQueensGame:
    def __init__(self, master, n):
        self.master = master
        self.n = n
        self.board = [['.' for _ in range(n)] for _ in range(n)]
        self.placed_queens = 0
        self.cell_size = 400 // self.n
        
        self.master.title(f"{n}-Queens Interactive Game")
        
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_board)
        self.reset_button.pack()
        
        self.draw_board()
    
    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
                
                if self.board[i][j] == 'Q':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="blue")

    def handle_click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        
        if self.board[row][col] == '.':
            if self.is_safe(row, col):
                self.board[row][col] = 'Q'
                self.placed_queens += 1
                self.draw_board()
                if self.placed_queens == self.n:
                    messagebox.showinfo("Congratulations!", "All queens placed correctly!")
                    self.reset_board()
            else:
                messagebox.showwarning("Invalid Move", "This position is not safe for a queen!")
        elif self.board[row][col] == 'Q':
            self.board[row][col] = '.'
            self.placed_queens -= 1
            self.draw_board()

    def is_safe(self, row, col):
        for i in range(self.n):
            if self.board[row][i] == 'Q' or self.board[i][col] == 'Q':
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 'Q':
                return False
        
        for i, j in zip(range(row, -1, -1), range(col, self.n)):
            if self.board[i][j] == 'Q':
                return False
        
        for i, j in zip(range(row, self.n), range(col, -1, -1)):
            if self.board[i][j] == 'Q':
                return False
        
        for i, j in zip(range(row, self.n), range(col, self.n)):
            if self.board[i][j] == 'Q':
                return False

        return True

    def reset_board(self):
        self.board = [['.' for _ in range(self.n)] for _ in range(self.n)]
        self.placed_queens = 0
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGame(root, 4)  
    root.mainloop()
