import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text=' ', font=('normal', 40), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, i, j):
        index = i * 3 + j
        if self.board[index] == ' ':
            self.make_move(index, self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif ' ' not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_move()

    def make_move(self, index, player):
        self.board[index] = player
        self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                self.buttons[i][j].config(text=self.board[index])

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.update_buttons()

    def ai_move(self):
        best_move = self.alpha_beta(self.board, 0, True, float('-inf'), float('inf'))
        if best_move is not None:
            self.make_move(best_move, 'O')

        if self.check_winner('O'):
            messagebox.showinfo("Game Over", "AI wins!")
            self.reset_board()
        elif ' ' not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
        else:
            self.current_player = 'X'

    def alpha_beta(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.alpha_beta(board, depth + 1, False, alpha, beta)
                    board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break  # Beta cut-off
            return best_move if depth == 0 else best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.alpha_beta(board, depth + 1, True, alpha, beta)
                    board[i] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return best_score

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
