# Window class that creates a basic window using the Tk interface

from tkinter import *
from tkinter import ttk

class Window:
	def __init__(self):
		# create window using Tk
		self.root = Tk()
		# make it easy to toggle fullscreen using the escape key
		self.root.bind("<Escape>",self.toggleFull)
		# default to fullscreen
		self.full = True
		self.root.attributes("-fullscreen",True)
		# update the window so the dimensions will be accurate for setting the size variable
		self.root.update()
		self.size = ((self.root.winfo_width()), (self.root.winfo_height()))
		
	def toggleFull(self,event):
		self.full = not(self.full)
		self.root.attributes("-fullscreen",self.full)

	def clearWindow(self):
		# delete all components of the root window
		for child in self.root.grid_slaves():
			child.grid_forget()

	def exit(self):
		# delete the root window
		self.root.destroy()
