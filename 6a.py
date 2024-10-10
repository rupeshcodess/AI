import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MissionariesAndCannibals:
    def __init__(self, master):
        self.master = master
        master.title("3 Missionaries and 3 Cannibals")

        self.left_missionaries = 3
        self.left_cannibals = 3
        self.right_missionaries = 0
        self.right_cannibals = 0
        self.boat_position = 'left'
        self.boat_missionaries = 0
        self.boat_cannibals = 0

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=800, height=400)
        self.canvas.pack()

        self.background_image = ImageTk.PhotoImage(Image.open("river_background.png").resize((800, 400)))
        self.boat_image = ImageTk.PhotoImage(Image.open("boat.png").resize((100, 100)))
        self.missionary_image = ImageTk.PhotoImage(Image.open("missionary.png").resize((50, 50)))
        self.cannibal_image = ImageTk.PhotoImage(Image.open("cannibal.png").resize((50, 50)))

        self.canvas.create_image(400, 200, image=self.background_image)
        self.boat = self.canvas.create_image(300, 300, image=self.boat_image)
        self.canvas.tag_bind(self.boat, "<Button-1>", self.cross_river)

        self.missionary_items = []
        self.cannibal_items = []

    def update_display(self):
        self.canvas.delete("missionary")
        self.canvas.delete("cannibal")

        x_offset = 50
        y_offset = 50

        self.missionary_items = []
        self.cannibal_items = []

        for i in range(self.left_missionaries):
            item = self.canvas.create_image(100, 100 + i * y_offset, image=self.missionary_image, tags="missionary")
            self.missionary_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='left': self.move_missionary(index, side))

        for i in range(self.left_cannibals):
            item = self.canvas.create_image(150, 100 + i * y_offset, image=self.cannibal_image, tags="cannibal")
            self.cannibal_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='left': self.move_cannibal(index, side))

        for i in range(self.right_missionaries):
            item = self.canvas.create_image(600, 100 + i * y_offset, image=self.missionary_image, tags="missionary")
            self.missionary_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='right': self.move_missionary(index, side))

        for i in range(self.right_cannibals):
            item = self.canvas.create_image(650, 100 + i * y_offset, image=self.cannibal_image, tags="cannibal")
            self.cannibal_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='right': self.move_cannibal(index, side))

        boat_x = 300 if self.boat_position == 'left' else 500
        self.canvas.coords(self.boat, boat_x, 300)

        for i in range(self.boat_missionaries):
            item = self.canvas.create_image(boat_x - 20, 250 + i * y_offset, image=self.missionary_image, tags="missionary")
            self.missionary_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='boat': self.move_missionary(index, side))

        for i in range(self.boat_cannibals):
            item = self.canvas.create_image(boat_x + 20, 250 + i * y_offset, image=self.cannibal_image, tags="cannibal")
            self.cannibal_items.append(item)
            self.canvas.tag_bind(item, "<Button-1>", lambda e, index=i, side='boat': self.move_cannibal(index, side))

    def move_missionary(self, index, side):
        if side == 'left' and self.left_missionaries > 0 and self.boat_missionaries + self.boat_cannibals < 2:
            self.left_missionaries -= 1
            self.boat_missionaries += 1
        elif side == 'right' and self.right_missionaries > 0 and self.boat_missionaries + self.boat_cannibals < 2:
            self.right_missionaries -= 1
            self.boat_missionaries += 1
        elif side == 'boat' and self.boat_missionaries > 0:
            if self.boat_position == 'left':
                self.left_missionaries += 1
            else:
                self.right_missionaries += 1
            self.boat_missionaries -= 1
        self.update_display()

    def move_cannibal(self, index, side):
        if side == 'left' and self.left_cannibals > 0 and self.boat_missionaries + self.boat_cannibals < 2:
            self.left_cannibals -= 1
            self.boat_cannibals += 1
        elif side == 'right' and self.right_cannibals > 0 and self.boat_missionaries + self.boat_cannibals < 2:
            self.right_cannibals -= 1
            self.boat_cannibals += 1
        elif side == 'boat' and self.boat_cannibals > 0:
            if self.boat_position == 'left':
                self.left_cannibals += 1
            else:
                self.right_cannibals += 1
            self.boat_cannibals -= 1
        self.update_display()

    def cross_river(self, event):
        if self.boat_missionaries == 0 and self.boat_cannibals == 0:
            messagebox.showwarning("Invalid Move", "The boat cannot cross without passengers!")
            return

        if self.boat_position == 'left':
            self.boat_position = 'right'
            self.right_missionaries += self.boat_missionaries
            self.right_cannibals += self.boat_cannibals
        else:
            self.boat_position = 'left'
            self.left_missionaries += self.boat_missionaries
            self.left_cannibals += self.boat_cannibals

        self.boat_missionaries = 0
        self.boat_cannibals = 0

        self.update_display()
        self.check_win_condition()
        self.check_lose_condition()

    def check_win_condition(self):
        if self.right_missionaries == 3 and self.right_cannibals == 3:
            messagebox.showinfo("Congratulations", "You solved the puzzle!")
            self.master.quit()

    def check_lose_condition(self):
        if (self.left_missionaries < self.left_cannibals and self.left_missionaries > 0) or (self.right_missionaries < self.right_cannibals and self.right_missionaries > 0):
            if messagebox.askyesno("Game Over", "Cannibals ate the missionaries! Do you want to play again?"):
                self.reset_game()
            else:
                self.master.quit()

    def reset_game(self):
        self.left_missionaries = 3
        self.left_cannibals = 3
        self.right_missionaries = 0
        self.right_cannibals = 0
        self.boat_position = 'left'
        self.boat_missionaries = 0
        self.boat_cannibals = 0
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = MissionariesAndCannibals(root)
    root.mainloop()
