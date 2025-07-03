import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multiscreen App")
        self.geometry("800x700")
        self.minsize(800, 600)

        self.frames = {}

        for F in (HomeFrame, SettingsFrame):
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
        button1 = ctk.CTkButton(self, text="START", command=lambda: parent.show_frame("SettingsFrame"))
        button2 = ctk.CTkButton(self, text="QUIT", command=lambda: parent.destroy())
        label.place(relx=0.3, rely=0, relwidth=0.4, relheight=0.1)
        button1.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.1)
        button2.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.1)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_running = False

        label = ctk.CTkLabel(self, text="Settings", font=("Arial", 24))
        home_button = ctk.CTkButton(self, text="Back to Home",command=lambda: parent.show_frame("HomeFrame"))

        home_button.place(x=650, y=110)
        # These guys need to be attributes in order to call them in functions
        self.pause_button = ctk.CTkButton(self, text="PAUSE", command=self.pause)
        self.play_button = ctk.CTkButton(self, text="PLAY", command=self.play)
        self.reset_button = ctk.CTkButton(self, text="RESET", command=self.reset)
        self.board = PuzzleBoard(self, 600, 600)

        self.play_button.place(x=650, y=140)
        self.pause_button.place(x=650, y=140)
        self.reset_button.place(x=650, y=170)
        self.board.place(x=200, y=100)

    def animate(self):
        if self.is_running == False:
            return None
        
        self.board.solve()
        self.after(2000, self.animate)

        
    def play(self):
        self.is_running = True
        self.pause_button.tkraise()
        self.board.after(500, self.animate)
    
    def pause(self):
        self.is_running = False
        self.play_button.tkraise()

    def reset(self):
        self.is_running = False
        self.play_button.tkraise()
        self.board.delete("all")
        self.board = PuzzleBoard(self, 600, 600)
        self.board.place(x=200, y=100)

        
class PuzzleBoard(tk.Canvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height)
        self.current_move = 0        
        
        audi_image = self.load_img("img/Audi.png")

        self.image_refs = audi_image
        self.audi = self.create_image(0, 0, image=audi_image, anchor='nw')

    def load_img(self, path):
        img = Image.open(path)
        img = img.resize((200, 100))
        img = ImageTk.PhotoImage(img)
        return img
    
    def solve(self):
        if self.current_move == 6:
            return
        self.move(self.audi, 0, 100)
        self.current_move += 1


if __name__ == "__main__":
    app = App()
    app.mainloop()
