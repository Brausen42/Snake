from tkinter import *
from tkinter import ttk

class Unit:
    def __init__(self,master,size,x,y,color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.master = master
        self.create()

    def create(self):
        self.unit = self.master.create_rectangle(self.x,
                                       self.y,
                                       self.x+self.size,
                                       self.y+self.size,
                                       fill=self.color,
                                       width = 0)

    def move(self,location):
        x = location[0]
        y = location[1]
        self.master.delete(self.unit)
        self.unit = self.master.create_rectangle(x,y,x+self.size,y+self.size, fill = self.color, width = 0)
        self.x = x
        self.y = y

    def getPosition(self):
        return (self.x,self.y)

    def destroy(self):
        self.master.delete(self.unit)
