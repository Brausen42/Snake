# SnakeGame class as an abstraction for what all SnakeGames contain

from Window import *
from Snake import *
from Food import *
import random
import math

class SnakeGame(Window):
	def __init__(self):
		super().__init__()
		self.root.title = "Snake"
		# set grid unit size
		self.snakeSize = 20
		# update root window to get an accurate grid size
		self.root.update()
		# set grid size based on window size
		self.grid = ((self.root.winfo_width()//self.snakeSize)-1, (self.root.winfo_height()//self.snakeSize)-1)
		self.startGame()
		# allow root window to handle input
		self.root.mainloop()

	def startGame(self):
		# cover root window with a canvas
		self.canvas = Canvas(self.root,
							 background = "black",
							 width = self.grid[0]*(self.snakeSize+1),
							 height = self.grid[1]*(self.snakeSize+1))
		self.canvas.grid(column = 0,
						row = 0,
						sticky=(N,S,E,W))
		# bind WASD to the appropriate movements
		self.root.bind("a",self.goLeft)
		self.root.bind("w",self.goUp)
		self.root.bind("s",self.goDown)
		self.root.bind("d",self.goRight)
		# allow pausing of the game
		self.root.bind("<space>",self.pauseGame)
		# create intial food
		self.food = Food(self.canvas,self.snakeSize,self.snakeSize*random.randint(0,self.grid[0]),self.snakeSize*random.randint(0,self.grid[1]),"yellow")
		# activate game with inital speed
		self.active = True
		self.pause = False
		self.speed = 100
		# all active locations
		self.occupied = {self.food.getPosition():[self.food.type]}

	# all directional changes are only allowed to be made once per game loop to prevent turning into self
	def goUp(self,event):
		if(event.keysym == "w"):
			snake = self.snakes[0]
		else:
			snake = self.snakes[1]
		if not(snake.direction == "DOWN") and not(snake.commit):
			snake.goUp()
			snake.commit = True
	def goDown(self,event):
		if(event.keysym == "s"):
			snake = self.snakes[0]
		else:
			snake = self.snakes[1]
		if not(snake.direction == "UP") and not(snake.commit):
			snake.goDown()
			snake.commit = True
	def goLeft(self,event):
		if(event.keysym == "a"):
			snake = self.snakes[0]
		else:
			snake = self.snakes[1]
		if not(snake.direction == "RIGHT") and not(snake.commit):
			snake.goLeft()
			snake.commit = True
	def goRight(self,event):
		if(event.keysym == "d"):
			snake = self.snakes[0]
		else:
			snake = self.snakes[1]
		if not(snake.direction == "LEFT") and not(snake.commit):
			snake.goRight()
			snake.commit = True

	def check(self,first,second):
		# check for collision between first and second
		for snake in self.snakes:
			if snake.getPosition() == second.getPosition():
				return True


	def newFood(self):
		self.occupied[self.food.getPosition()].remove(self.food.type)
		# adjust game speed
		self.speed = math.ceil(self.speed * .95)
		# destroy old food
		self.food.destroy()
		bad = True
		# find a valid (x,y) position for new food
		while bad:
			bad = False
			xpos = self.snakeSize*random.randint(0,self.grid[0])
			ypos = self.snakeSize*random.randint(0,self.grid[1])
			if (xpos,ypos) in self.occupied:
				bad = True
		# create the new food on the canvas
		self.food = Food(self.canvas,self.snakeSize,xpos,ypos,"yellow")
		if self.food.getPosition() in self.occupied:
			print("WARNING: food placed at location that already contains a unit")
			self.occupied[self.food.getPosition()].append(self.food.type)
		else:
			self.occupied[self.food.getPosition()] = [self.food.type]

	def pauseGame(self,event):
		if (not self.pause):
			self.pauseScreen = Frame(self.root)
			message = ttk.Label(self.pauseScreen,text="Paused",font="TkDefaultFont 48")
			score = ttk.Label(self.pauseScreen,text = "Current score is: " + str(self.snakes[0].length))
			note = ttk.Label(self.pauseScreen,text = "Press space to continue")

			message.grid()
			score.grid()
			note.grid()

			self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=self.pauseScreen)
		else:
			self.pauseScreen.destroy()

		self.pause = not(self.pause)
		self.loop()

	def end(self):
		self.active = False
		frame = Frame(self.root)
		message = ttk.Label(frame,text="You have lost",font="TkDefaultFont 48")
		score = ttk.Label(frame,text = "Your score is " + str(self.snakes[0].length))
		restart = Button(frame,text = "Restart",command=self.startGame)
		menu = Button(frame,text = "Main Menu", command=self.snakeMenu)

		message.grid()
		score.grid()
		restart.grid()
		menu.grid()

		self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

	def collide(self,snake):
		pos = snake.getPosition()
		for snakes in self.snakes:
			if snake != snakes:
				if pos == snakes.getPosition():
					return True
			for unit in snakes.body[1:]:
				if pos == unit.getPosition():
					return True
		return False

	def loop(self):
		if not(self.pause) and self.active:
			for snake in self.snakes:
				snake.move(self.occupied)
				if self.check(snake,self.food):
					snake.anotherOne()
					self.newFood()
				snake.commit = False
			for snake in self.snakes:
				if self.collide(snake):
					self.end()
			self.root.after(self.speed,self.loop)

	def snakeMenu(self):
		self.exit()
		from SnakeMenu import SnakeMenu
		SnakeMenu()
