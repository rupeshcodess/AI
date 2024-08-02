import tkinter as tk
from tkinter import messagebox

class TowerOfHanoiGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Tower of Hanoi Game")
        self.canvas_width = 600
        self.canvas_height = 400
        self.peg_width = 10
        self.disk_height = 20
        self.num_disks = 3

        self.pegs = {
            'A': [],
            'B': [],
            'C': []
        }

        self.selected_disk = None

        self.create_widgets()
        self.create_pegs()

    def create_widgets(self):
        self.disk_entry_label = tk.Label(self.master, text="Number of Disks:")
        self.disk_entry_label.pack()

        self.disk_entry = tk.Entry(self.master)
        self.disk_entry.pack()
        self.disk_entry.insert(0, "3")

        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.pack()

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def create_pegs(self):
        peg_positions = self.get_peg_positions()
        self.canvas.create_line(peg_positions['A'], 0, peg_positions['A'], self.canvas_height, width=self.peg_width, fill="black")
        self.canvas.create_line(peg_positions['B'], 0, peg_positions['B'], self.canvas_height, width=self.peg_width, fill="black")
        self.canvas.create_line(peg_positions['C'], 0, peg_positions['C'], self.canvas_height, width=self.peg_width, fill="black")

    def get_peg_positions(self):
        return {
            'A': self.canvas_width // 4,
            'B': self.canvas_width // 2,
            'C': 3 * self.canvas_width // 4
        }

    def create_disks(self):
        self.pegs = {'A': [], 'B': [], 'C': []}
        peg_positions = self.get_peg_positions()
        initial_peg_x = peg_positions['A']

        self.disks = []
        disk_width = 100
        width_step = 20

        for i in range(self.num_disks):
            width = disk_width - i * width_step
            color = self.get_color(i)
            disk_id = self.canvas.create_rectangle(initial_peg_x - width // 2, self.canvas_height - (i + 1) * self.disk_height,
                                                   initial_peg_x + width // 2, self.canvas_height - i * self.disk_height,
                                                   fill=color)
            self.disks.append(disk_id)
            self.pegs['A'].append(disk_id)

    def get_color(self, index):
        colors = ["green", "red", "orange", "blue", "purple"]
        return colors[index % len(colors)]

    def start_game(self):
        try:
            self.num_disks = int(self.disk_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of disks.")
            return

        if self.num_disks < 1:
            messagebox.showerror("Invalid Input", "Please enter a number greater than 0.")
            return

        self.canvas.delete("all")
        self.create_pegs()
        self.create_disks()

    def on_canvas_click(self, event):
        peg_positions = self.get_peg_positions()
        peg_keys = list(peg_positions.keys())
        peg_distances = {key: abs(event.x - pos) for key, pos in peg_positions.items()}
        nearest_peg = min(peg_distances, key=peg_distances.get)

        if self.selected_disk is None:
            self.select_disk(nearest_peg)
        else:
            self.move_selected_disk(nearest_peg)

    def select_disk(self, peg):
        if self.pegs[peg]:
            self.selected_disk = self.pegs[peg][-1]
            self.canvas.itemconfig(self.selected_disk, outline="yellow", width=2)

    def move_selected_disk(self, target_peg):
        if self.selected_disk is None:
            return

        source_peg = self.get_disk_peg(self.selected_disk)
        
        if source_peg != target_peg:
            if self.is_valid_move(source_peg, target_peg):
                self.pegs[source_peg].pop()
                self.pegs[target_peg].append(self.selected_disk)
                self.update_disk_position(self.selected_disk, target_peg)
                if self.is_game_won():
                    messagebox.showinfo("Congratulations!", "You solved the Tower of Hanoi!")
            else:
                messagebox.showwarning("Invalid Move", "You cannot place a larger disk on a smaller one.")
        
        self.canvas.itemconfig(self.selected_disk, outline="", width=1)
        self.selected_disk = None

    def is_valid_move(self, source_peg, target_peg):
        if not self.pegs[target_peg]:
            return True
        top_target_disk = self.pegs[target_peg][-1]
        selected_disk_bbox = self.canvas.bbox(self.selected_disk)
        top_target_disk_bbox = self.canvas.bbox(top_target_disk)
        return selected_disk_bbox[2] - selected_disk_bbox[0] < top_target_disk_bbox[2] - top_target_disk_bbox[0]

    def get_disk_peg(self, disk_id):
        for peg, disks in self.pegs.items():
            if disk_id in disks:
                return peg
        return None

    def update_disk_position(self, disk_id, target_peg):
        peg_positions = self.get_peg_positions()
        target_x = peg_positions[target_peg]
        disk_index = len(self.pegs[target_peg]) - 1
        disk_width = self.canvas.bbox(disk_id)[2] - self.canvas.bbox(disk_id)[0]

        self.canvas.coords(disk_id,
                           target_x - disk_width // 2, self.canvas_height - (disk_index + 1) * self.disk_height,
                           target_x + disk_width // 2, self.canvas_height - disk_index * self.disk_height)

    def is_game_won(self):
        return len(self.pegs['C']) == self.num_disks

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiGame(root)
    root.mainloop()
