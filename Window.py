from tkinter import *
from tkinter import ttk

class Window:
    def __init__(self):
        self.full = True

        self.root = Tk()
        self.root.bind("<Escape>",self.toggleFull)
        self.root.attributes("-fullscreen",True)
        self.root.update()
        self.size = ((self.root.winfo_width()), (self.root.winfo_height()))
        
    def toggleFull(self,event):
        self.full = not(self.full)
        self.root.attributes("-fullscreen",self.full)

    def clearWindow(self):
        for child in self.root.grid_slaves():
            child.grid_forget()

    def exit(self):
        self.root.destroy()
