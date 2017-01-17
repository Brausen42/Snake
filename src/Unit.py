# Unit class that is used to represent a unit on a gridded Tk canvas object

from tkinter import *
from tkinter import ttk
from enum import Enum

class UnitType(Enum):
	unit = 0
	food = 1
	mine = 2

class Unit:
	def __init__(self,master,size,x,y,color):
		self.x = x
		self.y = y
		self.size = size
		self.color = color
		self.master = master
		self.type = UnitType.unit

		self.create()

	def create(self):
		# places a default "size X size" square on the master canvas at the specified location (x,y)
		self.unit = self.master.create_rectangle(self.x,
									   self.y,
									   self.x+self.size,
									   self.y+self.size,
									   fill=self.color,
									   width = 0)

	def move(self,location):
		# set new location
		self.x = location[0]
		self.y = location[1]
		# delete unit at old location
		self.master.delete(self.unit)
		# create new unit at new location
		self.unit = self.master.create_rectangle(self.x,
												self.y,
												self.x+self.size,
												self.y+self.size,
												fill = self.color,
												width = 0)

	def getPosition(self):
		return (self.x,self.y)

	def destroy(self):
		# remove unit from master canvas
		self.master.delete(self.unit)
