import customtkinter as ctk
from vehicle import Vehicle, V, H
from state import State
from solver import BFSSolver, IDSSolver, UCSSolver, AStarSolver
from Map import maps
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme('dark-blue')

        self.title("Rush Hour")
        self.geometry("800x700")
        self.minsize(800, 700)
        self.maxsize(800, 700)
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
        super().__init__(parent, fg_color='lightblue')
        
        label = ctk.CTkLabel(self, text="RUSH HOUR SOLVER", font=("Arial", 24))
        button1 = ctk.CTkButton(self, text="START", command=lambda: parent.show_frame("SolverFrame"))
        button2 = ctk.CTkButton(self, text="QUIT", command=lambda: parent.destroy())
        label.place(relx=0.3, rely=0, relwidth=0.4, relheight=0.1)
        button1.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.1)
        button2.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.1)

class SolverFrame(ctk.CTkFrame):
    last_algo = None

    def __init__(self, parent):
        super().__init__(parent, fg_color='lightblue')

        # Init but not yet intereacted
        self.move_list = None
        self.cost_list = None
        self.is_running = False
        self.after_id = None
        self.current_move = 0

        # Home sweet home
        home_button = ctk.CTkButton(self, text="Back to Home", command=lambda: self.go_home(parent))
        home_button.place(x=650, y=80)
        
        # Map options
        map_options = [f"MAP {i:02}" for i in range(1, 11)]
        self.map = ctk.StringVar(value='MAP 01')
        map_menu = ScrollableButton(self, options=map_options, textvariable=self.map, command=self.update_map)

        map_menu.place(x=650, y=150)

        # Algorithm options
        algorithm_options = ['BFS', 'IDS', 'UCS', 'A*']
        self.algorithm = ctk.StringVar(value='BFS')
        algorithm_menu = ScrollableButton(self, options=algorithm_options, textvariable=self.algorithm)

        algorithm_menu.place(x=650, y=180)

        # Functional buttons
        self.pause_button = ctk.CTkButton(self, text="PAUSE", command=self.pause)
        self.play_button = ctk.CTkButton(self, text="PLAY", command=self.play)
        reset_button = ctk.CTkButton(self, text="RESET", command=self.reset)
        solve_button = ctk.CTkButton(self, text="SOLVE", command=self.solve)

        self.play_button.place(x=650, y=210)
        self.pause_button.place(x=650, y=210)
        reset_button.place(x=650, y=240)
        solve_button.place(x=650, y=400)

        # Message displayer
        self.message_displayer = ctk.CTkLabel(self, text="", width=120)
        self.message_displayer.place(x=725, y=450, anchor='center')

        # Steps and costs displayer
        self.step_button = ctk.CTkButton(self, text="STEP\n", height=60)
        self.cost_button = ctk.CTkButton(self, text="COST\n", height=60)

        self.step_button.place(x=10, y=80)
        self.cost_button.place(x=10, y=140)
        # Render the first map
        
        self.load_map()
        self.board = PuzzleBoard(self, 600, 600).create_vehicle_list(self.vehicle_list)
        self.board.place(x=200, y=100)

    def animate(self):
        if self.is_running == False:
            return None
        
        if self.current_move == len(self.move_list):
            self.display_message("Done! Please reset!")
            self.play_button.tkraise()
            return None
        
        self.board.solve(self.current_move)
        self.step_button.configure(text=f"STEP\n{self.current_move + 1}")
        current_cost = self.cost_list[self.current_move] if self.cost_list else ""
        self.cost_button.configure(text=f"COST\n{current_cost}")
        self.current_move += 1

        self.after_id = self.after(1800, self.animate)

    def display_message(self, text):
        self.message_displayer.configure(text=text)

    def load_map(self):
        map = self.map.get()
        function_name = "make_" + map.lower().replace(" ", "_")

        self.vehicle_list = getattr(maps, function_name)()

    def play(self):
        if self.move_list == None:
            self.display_message("Please solve!")
            return
        
        if self.current_move == len(self.move_list):
            self.display_message("Done!")
            self.pause()
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

        self.play_button.tkraise()

        self.board.clear_vehicle()
        self.board.create_vehicle_list(self.vehicle_list)

        self.step_button.configure(text="STEP\n")
        self.cost_button.configure(text="COST\n")

        self.is_running = False
        self.after_id = None
        self.current_move = 0

    def solve(self):
        algorithm = self.algorithm.get()

        self.display_message(f"{algorithm} running!")

        initital_state = State(self.vehicle_list)
        
        if algorithm == 'IDS':
            solver = IDSSolver(initital_state)
        elif algorithm == 'BFS':
            solver = BFSSolver(initital_state)
        elif algorithm == 'UCS':
            solver = UCSSolver(initital_state)
        else:
            solver = AStarSolver(initital_state)
        
        path, moves, costs = solver.solve()
        
        if path is None:
            self.display_message("No solution !!!")
            return
        
        self.display_message("Solved!")
        self.move_list = moves
        self.cost_list = costs
        self.board.create_move_list(moves)

    def update_map(self):
        map = self.map.get()

        self.load_map()
        
        self.reset()

        self.move_list = None
        self.cost_list = None

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

    def clear_vehicle(self):
        for vehicle in self.vehicle_list:
            self.delete(vehicle)

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

    def solve(self, current_move):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        if self.move_list == None:
            return
        
        if current_move == len(self.move_list):
            return
        
        id, step = self.move_list[current_move]

        self.slide(self.vehicle_list[id], self.orientation_list[id], step)

    def slide(self, car, orientation, step, cnt=0):
        if cnt == 50:
            return
        
        if orientation == H:
            self.move(car, 2 * step, 0)
        else:
            self.move(car, 0, 2 * step)

        self.after_id = self.after(16, lambda: self.slide(car, orientation, step, cnt + 1))

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
