import tkinter as tk
from tkinter import messagebox

class WaterJugGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Problem Game")

        self.jug1_capacity = 5
        self.jug2_capacity = 3
        self.jug1 = 0
        self.jug2 = 0
        self.target_amount = 4

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        tk.Label(self.root, text="Jug 1 Capacity:").grid(row=0, column=0, padx=10, pady=5)
        self.jug1_capacity_entry = tk.Entry(self.root)
        self.jug1_capacity_entry.grid(row=0, column=1, padx=10, pady=5)
        self.jug1_capacity_entry.insert(0, self.jug1_capacity)

        tk.Label(self.root, text="Jug 2 Capacity:").grid(row=1, column=0, padx=10, pady=5)
        self.jug2_capacity_entry = tk.Entry(self.root)
        self.jug2_capacity_entry.grid(row=1, column=1, padx=10, pady=5)
        self.jug2_capacity_entry.insert(0, self.jug2_capacity)

        tk.Button(self.root, text="Update Capacities", command=self.update_capacities).grid(row=2, column=0, columnspan=2, pady=10)

        self.canvas1 = tk.Canvas(self.root, width=100, height=300, bg="white", borderwidth=2, relief="solid")
        self.canvas1.grid(row=3, column=0, padx=10, pady=10)

        self.canvas2 = tk.Canvas(self.root, width=100, height=300, bg="white", borderwidth=2, relief="solid")
        self.canvas2.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Fill Jug 1", command=self.fill_jug1).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Fill Jug 2", command=self.fill_jug2).grid(row=4, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Empty Jug 1", command=self.empty_jug1).grid(row=5, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Empty Jug 2", command=self.empty_jug2).grid(row=5, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Transfer Jug 1 -> Jug 2", command=self.transfer_jug1_to_jug2).grid(row=6, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Transfer Jug 2 -> Jug 1", command=self.transfer_jug2_to_jug1).grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Check Target", command=self.check_target).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Reset", command=self.reset).grid(row=8, column=0, columnspan=2, pady=10)

        self.status_display = tk.Label(self.root, text="")
        self.status_display.grid(row=9, column=0, columnspan=2, pady=10)

    def update_capacities(self):
        try:
            self.jug1_capacity = int(self.jug1_capacity_entry.get())
            self.jug2_capacity = int(self.jug2_capacity_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for jug capacities.")
            return

        if self.jug1 > self.jug1_capacity:
            self.jug1 = self.jug1_capacity
        if self.jug2 > self.jug2_capacity:
            self.jug2 = self.jug2_capacity

        self.update_display()

    def update_display(self):
        self.canvas1.delete("all")
        self.canvas1.create_rectangle(10, 300 - (self.jug1 / self.jug1_capacity) * 300, 90, 300, fill="blue", outline="black")
        self.canvas1.create_text(50, 310, text=f"{self.jug1}L", font=('Helvetica', 12))

        self.canvas2.delete("all")
        self.canvas2.create_rectangle(10, 300 - (self.jug2 / self.jug2_capacity) * 300, 90, 300, fill="blue", outline="black")
        self.canvas2.create_text(50, 310, text=f"{self.jug2}L", font=('Helvetica', 12))

    def fill_jug1(self):
        self.jug1 = self.jug1_capacity
        self.update_display()

    def fill_jug2(self):
        self.jug2 = self.jug2_capacity
        self.update_display()

    def empty_jug1(self):
        self.jug1 = 0
        self.update_display()

    def empty_jug2(self):
        self.jug2 = 0
        self.update_display()

    def transfer_jug1_to_jug2(self):
        transfer_amount = min(self.jug1, self.jug2_capacity - self.jug2)
        self.jug1 -= transfer_amount
        self.jug2 += transfer_amount
        self.update_display()

    def transfer_jug2_to_jug1(self):
        transfer_amount = min(self.jug2, self.jug1_capacity - self.jug1)
        self.jug2 -= transfer_amount
        self.jug1 += transfer_amount
        self.update_display()

    def check_target(self):
        if self.jug1 == self.target_amount or self.jug2 == self.target_amount:
            self.status_display.config(text="Target amount reached!")
        else:
            self.status_display.config(text="Target amount not reached. Keep trying!")

    def reset(self):
        self.jug1 = 0
        self.jug2 = 0
        self.update_display()
        self.status_display.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugGame(root)
    root.mainloop()
