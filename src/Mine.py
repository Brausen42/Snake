from Unit import *

class Mine(Unit):
	def __init__(self,master,size,x,y,color):
		super().__init__(master,size,x,y,color)

	def create(self):
		self.unit = self.master.create_polygon(self.x,
										  self.y+self.size,
										  self.x+(self.size/2),
										  self.y,
										  self.x+self.size,
										  self.y+self.size,
										  fill=self.color,
										  width = 0)
