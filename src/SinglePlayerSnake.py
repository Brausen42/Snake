from SnakeGame import *
from Mine import *

class SinglePlayerSnake(SnakeGame):
	def __init__(self):
		super().__init__()

	def startGame(self):
		super().startGame()

		self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), "green",self.grid)]
		# TODO: make getting the type of the snake less error prone
		self.occupied[self.snakes[0].getPosition()] = [self.snakes[0].body[0].type]

		self.mines = []

		self.loop()

	def loop(self):
		if not(self.pause) and self.active:
			if (not self.snakes[0].move(self.occupied)) or self.checkMine(self.mines):
				self.end()
			if self.check(self.snakes[0],self.food):
				self.snakes[0].anotherOne()
				if (self.snakes[0].length % 3) == 0:
					self.createMine()
				self.newFood()
			self.snakes[0].commit = False
			for snake in self.snakes:
				if self.collide(snake):
					self.end()
			self.root.after(self.speed,self.loop)


	def createMine(self):
		bad = True
		while(bad):
			bad = False
			xpos = self.snakeSize*random.randint(0,self.grid[0])
			ypos = self.snakeSize*random.randint(0,self.grid[1])
			for mine in self.mines:
				if mine.getPosition == (xpos,ypos):
					bad = True
			for snake in self.snakes:
				if (xpos,ypos) in snake.getPositionList():
					bad = True

		self.mines.append(Mine(self.canvas,self.snakeSize,self.snakeSize*random.randint(0,self.grid[0]),self.snakeSize*random.randint(0,self.grid[1]),"red"))
		if self.mines[-1].getPosition() in self.occupied:
			print("WARNING: mine placed at location that already contains a unit")
			self.occupied[self.mines[-1].getPosition()].append(self.mines[-1].type)
		else:
			self.occupied[self.mines[-1].getPosition()] = [self.mines[-1].type]

	def checkMine(self,mines):
		for mine in mines:
			for snake in self.snakes:
				if snake.getPosition() == mine.getPosition():
					return True
