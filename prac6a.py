import tkinter as tk
from tkinter import messagebox
from collections import deque

class State:
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None

    def is_goal(self):
        return self.cannibalLeft == 0 and self.missionaryLeft == 0

    def is_valid(self):
        return (self.missionaryLeft >= 0 and self.missionaryRight >= 0 and
                self.cannibalLeft >= 0 and self.cannibalRight >= 0 and
                (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) and
                (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight))

    def __eq__(self, other):
        return (self.cannibalLeft == other.cannibalLeft and
                self.missionaryLeft == other.missionaryLeft and
                self.boat == other.boat and
                self.cannibalRight == other.cannibalRight and
                self.missionaryRight == other.missionaryRight)

    def __hash__(self):
        return hash((self.cannibalLeft, self.missionaryLeft, self.boat, self.cannibalRight, self.missionaryRight))

def successors(cur_state):
    children = []
    if cur_state.boat == 'left':
        new_states = [
            State(cur_state.cannibalLeft - 2, cur_state.missionaryLeft, 'right',
                  cur_state.cannibalRight + 2, cur_state.missionaryRight),
            State(cur_state.cannibalLeft, cur_state.missionaryLeft - 2, 'right',
                  cur_state.cannibalRight, cur_state.missionaryRight + 2),
            State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft - 1, 'right',
                  cur_state.cannibalRight + 1, cur_state.missionaryRight + 1),
            State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft, 'right',
                  cur_state.cannibalRight + 1, cur_state.missionaryRight),
            State(cur_state.cannibalLeft, cur_state.missionaryLeft - 1, 'right',
                  cur_state.cannibalRight, cur_state.missionaryRight + 1)
        ]
    else:
        new_states = [
            State(cur_state.cannibalLeft + 2, cur_state.missionaryLeft, 'left',
                  cur_state.cannibalRight - 2, cur_state.missionaryRight),
            State(cur_state.cannibalLeft, cur_state.missionaryLeft + 2, 'left',
                  cur_state.cannibalRight, cur_state.missionaryRight - 2),
            State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft + 1, 'left',
                  cur_state.cannibalRight - 1, cur_state.missionaryRight - 1),
            State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft, 'left',
                  cur_state.cannibalRight - 1, cur_state.missionaryRight),
            State(cur_state.cannibalLeft, cur_state.missionaryLeft + 1, 'left',
                  cur_state.cannibalRight, cur_state.missionaryRight - 1)
        ]

    for state in new_states:
        if state.is_valid():
            state.parent = cur_state
            children.append(state)

    return children

def bfs(start_state, goal_state):
    frontier = deque([start_state])
    explored = set()
    while frontier:
        state = frontier.popleft()
        if state == goal_state:
            return state
        explored.add(state)
        for child in successors(state):
            if child not in explored and child not in frontier:
                child.parent = state
                frontier.append(child)
    return None

class MissionariesCannibalsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Missionaries and Cannibals Game")

        
        self.current_state = State(3, 3, 'left', 0, 0)
        self.history = [self.current_state]

        
        self.canvas = tk.Canvas(root, width=800, height=300, bg='lightblue')
        self.canvas.pack()

        self.state_label = tk.Label(root, text=self.get_state_text())
        self.state_label.pack()

        self.move_frame = tk.Frame(root)
        self.move_frame.pack()

        self.cannibals_left_var = tk.IntVar(value=0)
        self.missionaries_left_var = tk.IntVar(value=0)
        self.cannibals_right_var = tk.IntVar(value=0)
        self.missionaries_right_var = tk.IntVar(value=0)

        self.cannibals_left_label = tk.Label(self.move_frame, text="Cannibals Left:")
        self.cannibals_left_label.grid(row=0, column=0)
        self.cannibals_left_spinbox = tk.Spinbox(self.move_frame, from_=0, to=3, textvariable=self.cannibals_left_var)
        self.cannibals_left_spinbox.grid(row=0, column=1)

        self.missionaries_left_label = tk.Label(self.move_frame, text="Missionaries Left:")
        self.missionaries_left_label.grid(row=1, column=0)
        self.missionaries_left_spinbox = tk.Spinbox(self.move_frame, from_=0, to=3, textvariable=self.missionaries_left_var)
        self.missionaries_left_spinbox.grid(row=1, column=1)

        self.cannibals_right_label = tk.Label(self.move_frame, text="Cannibals Right:")
        self.cannibals_right_label.grid(row=2, column=0)
        self.cannibals_right_spinbox = tk.Spinbox(self.move_frame, from_=0, to=3, textvariable=self.cannibals_right_var)
        self.cannibals_right_spinbox.grid(row=2, column=1)

        self.missionaries_right_label = tk.Label(self.move_frame, text="Missionaries Right:")
        self.missionaries_right_label.grid(row=3, column=0)
        self.missionaries_right_spinbox = tk.Spinbox(self.move_frame, from_=0, to=3, textvariable=self.missionaries_right_var)
        self.missionaries_right_spinbox.grid(row=3, column=1)

        self.move_button = tk.Button(root, text="Move", command=self.perform_move)
        self.move_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.auto_solve_button = tk.Button(root, text="Auto Solve", command=self.auto_solve)
        self.auto_solve_button.pack()

        self.solution_text = tk.Text(root, height=10, width=50)
        self.solution_text.pack()

        self.update_canvas()

    def get_state_text(self):
        return (f"Left Bank: {self.current_state.missionaryLeft} Missionaries, {self.current_state.cannibalLeft} Cannibals\n"
                f"Right Bank: {self.current_state.missionaryRight} Missionaries, {self.current_state.cannibalRight} Cannibals\n"
                f"Boat is on the {self.current_state.boat} bank")

    def perform_move(self):
        try:
            cannibals_left = self.cannibals_left_var.get()
            missionaries_left = self.missionaries_left_var.get()
            cannibals_right = self.cannibals_right_var.get()
            missionaries_right = self.missionaries_right_var.get()

            if self.current_state.boat == 'left':
                new_state = State(
                    self.current_state.cannibalLeft - cannibals_left,
                    self.current_state.missionaryLeft - missionaries_left,
                    'right',
                    self.current_state.cannibalRight + cannibals_left,
                    self.current_state.missionaryRight + missionaries_right
                )
            else:
                new_state = State(
                    self.current_state.cannibalLeft + cannibals_left,
                    self.current_state.missionaryLeft + missionaries_left,
                    'left',
                    self.current_state.cannibalRight - cannibals_left,
                    self.current_state.missionaryRight - missionaries_right
                )

            if new_state.is_valid():
                self.current_state = new_state
                self.history.append(self.current_state)
                self.state_label.config(text=self.get_state_text())
                self.update_canvas()
                if self.current_state.is_goal():
                    messagebox.showinfo("Congratulations!", "You have solved the puzzle!")
            else:
                messagebox.showerror("Invalid Move", "The move is not valid.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset(self):
        self.current_state = State(3, 3, 'left', 0, 0)
        self.history = [self.current_state]
