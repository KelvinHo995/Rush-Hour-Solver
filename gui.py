import customtkinter as ctk
import tkinter as tk
from vehicle import Vehicle, V, H
from state import State
from a_star_solver import a_star_solver
from recursive_dfs import ids_solver

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multiscreen App")
        self.geometry("800x700")
        self.minsize(800, 600)

        self.frames = {}

        for F in (HomeFrame, SolverFrame):
            frame = F(parent=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        
        self.show_frame("HomeFrame")
    
    def show_frame(self, name):
        """Show frame from the given name"""
        frame = self.frames[name]
        frame.tkraise()

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        label = ctk.CTkLabel(self, text="RUSH HOUR SOLVER", font=("Arial", 24))
        button1 = ctk.CTkButton(self, text="START", command=lambda: parent.show_frame("SolverFrame"))
        button2 = ctk.CTkButton(self, text="QUIT", command=lambda: parent.destroy())
        label.place(relx=0.3, rely=0, relwidth=0.4, relheight=0.1)
        button1.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.1)
        button2.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.1)

class SolverFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
        ve2 = Vehicle((1 << 43) | (1 << 35), V)  
        ve3 = Vehicle((1 << 34) | (1 << 42) | (1 << 50), V)
        ve4 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
        ve5 = Vehicle((1 << 26) | (1 << 25), H)
        ve6 = Vehicle((1 << 28) | (1 << 20), V)
        ve7 = Vehicle((1 << 27) | (1 << 19), V)
        ve8 = Vehicle((1 << 14) | (1 << 13), H)
        ve9 = Vehicle((1 << 10) | (1 << 9), H)
        self.vehicle_list = [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9]

        # path, moves = dfs_solver(State(self.vehicle_list), max_depth=25)
        self.move_list = None
        self.is_running = False
        self.after_id = None

        home_button = ctk.CTkButton(self, text="Back to Home", command=lambda: self.go_home(parent))
        home_button.place(x=650, y=80)
        solve_button = ctk.CTkButton(self, text="Solve", command=self.solve)
        solve_button.place(x=650, y=400)

        self.message_displayer = ctk.CTkLabel(self, text="", width=120)
        self.message_displayer.place(x=725, y=450, anchor='center')

        # These guys need to be attributes in order to call them in functions
        self.pause_button = ctk.CTkButton(self, text="PAUSE", command=self.pause)
        self.play_button = ctk.CTkButton(self, text="PLAY", command=self.play)
        self.reset_button = ctk.CTkButton(self, text="RESET", command=self.reset)
        self.board = None

        self.play_button.place(x=650, y=210)
        self.pause_button.place(x=650, y=240)
        self.reset_button.place(x=650, y=270)

        # Algorithm options
        algorithm_options = ['DFS', 'BFS', 'UCS', 'A*']
        self.algorithm = ctk.StringVar(value='DFS')
        algorithm_menu = ScrollableButton(self, options=algorithm_options, textvariable=self.algorithm)

        algorithm_menu.place(x=650, y=180)

        # Map options
        map_options = [f"MAP {i:02}" for i in range(1, 11)]
        self.map = ctk.StringVar(value='MAP 01')
        map_menu = ScrollableButton(self, options=map_options, textvariable=self.map, command=self.update_map)

        map_menu.place(x=650, y=150)

        self.update_map()


    def animate(self):
        if self.is_running == False:
            return None
        
        self.board.solve()

        self.after_id = self.after(1800, self.animate)

    def display_message(self, text):
        self.message_displayer.configure(text=text)

    def load_map(self):
        self.vehicle_list = []
        with open(f"Map/{self.map}.txt", "r", encoding="utf-8") as f:
            for line in f:
                mask, orientation = map(int, line.split())
                self.vehicle_list.append(Vehicle(mask, orientation))

    def play(self):
        if self.move_list == None:
            self.display_message("Please solve!")
            return
        
        self.is_running = True
        self.display_message("Playing!")
        self.pause_button.tkraise()

        self.after_id = self.board.after(500, self.animate)
    
    def pause(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.is_running = False
        self.display_message("Pausing!")
        self.play_button.tkraise()

    def reset(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.is_running = False

        self.play_button.tkraise()

        if self.board.moved():
            self.board.destroy()
            self.board = PuzzleBoard(self, 600, 600).create_vehicle_list(self.vehicle_list)
            self.board.place(x=200, y=100)

    def solve(self):
        if self.move_list != None:
            return

        initital_state = State(self.vehicle_list)
        solver = None

        algorithm = self.algorithm.get()
        if algorithm == 'DFS':
            pass
        elif algorithm == 'BFS':
            pass
        elif algorithm == 'UCS':
            pass
        else:
            pass
        
        self.display_message(f"{algorithm} running!")
        path, moves, costs = solver.solve()

    def update_map(self):
        map = self.map.get()

        # self.vehicle_list = self.load_vehicle()
        
        if self.board != None:
            self.board.destroy()
        self.board = PuzzleBoard(self, 600, 600).create_vehicle_list(self.vehicle_list)
        self.board.place(x=200, y=100)

        self.display_message(f"{map} loaded!")

    def go_home(self, parent):
        self.reset()
        parent.show_frame("HomeFrame")

class PuzzleBoard(ctk.CTkCanvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height, borderwidth=2, relief="solid")
        self.current_move = 0        
        self.after_id = None
        self.vehicle_list = None
        self.orientation_list = None
        self.move_list = None

        self.draw_grid()

    def create_move_list(self, move_list):
        self.move_list = move_list

    def create_vehicle_list(self, vehicle_list):
        self.vehicle_list = []
        self.orientation_list = []

        for i, vehicle in enumerate(vehicle_list):

            # Rectangle corners, orientation and grid length
            row, col = vehicle.get_position()
            x1 = col * 100 + 3
            y1 = row * 100 + 3
            orientation = vehicle.get_orientation()
            length = vehicle.get_weight()

            if orientation == H:
                x2 = (col + length) * 100 - 3
                y2 = (row + 1) * 100 - 3
            else:
                x2 = (col+ 1) * 100 - 3
                y2 = (row + length) * 100 - 3

            # Color 
            if i == 0:
                color = 'red'
            elif length == 2:
                color = 'blue'
            else:
                color = 'green'

            # Append
            self.vehicle_list.append(self.create_round_rectangle(x1, y1, x2, y2, fill=color))
            self.orientation_list.append(vehicle.get_orientation())

        return self
    
    def create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)
    
    def draw_grid(self):
        THICKNESS = 2
        COLOR = 'black'
        HEIGHT = 600
        WIDTH = 600
        ROW = 6
        COL = 6
        ROW_HEIGHT = 100
        COL_WIDTH = 100

        for i in range(ROW):
            y = i * ROW_HEIGHT
            self.create_line(0, y, 605, y, fill=COLOR, width=THICKNESS)

        # Draw vertical lines
        for i in range(COL):
            x = i * COL_WIDTH
            self.create_line(x, 0, x, 605, fill=COLOR, width=THICKNESS)

    def solve(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        if self.current_move == len(self.move_list):
            return
        
        id, step = self.move_list[self.current_move]

        self.slide(self.vehicle_list[id], self.orientation_list[id], step)

        self.current_move += 1
    
    def slide(self, car, orientation, step, cnt=0):
        if cnt == 50:
            return
        
        if orientation == H:
            self.move(car, 2 * step, 0)
        else:
            self.move(car, 0, 2 * step)

        self.after_id = self.after(16, lambda: self.slide(car, orientation, step, cnt + 1))

    def moved(self):
        return self.current_move > 0


class ScrollableButton(ctk.CTkButton):
    def __init__(self, parent, options, textvariable, **kwargs):
        super().__init__(parent, textvariable=textvariable, **kwargs)
        self.options = options
        self.index = 0
        self.var = textvariable

        # Bind mouse scroll events
        self.bind("<MouseWheel>", self.on_mousewheel)        # Windows/macOS
        self.bind("<Button-4>", self.on_mousewheel_linux)    # Linux scroll up
        self.bind("<Button-5>", self.on_mousewheel_linux)    # Linux scroll down
    
    def update_var(self):
        self.var.set(self.options[self.index])

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.index = (self.index - 1) % len(self.options)
        else:
            self.index = (self.index + 1) % len(self.options)
        self.update_var()

    def on_mousewheel_linux(self, event):
        if event.num == 4:
            self.index = (self.index - 1) % len(self.options)
        elif event.num == 5:
            self.index = (self.index + 1) % len(self.options)
        self.update_var()

if __name__ == "__main__":
    app = App()
    app.mainloop()
