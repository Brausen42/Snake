from SnakeGame import *

class PlayerVsAISnake(SnakeGame):
	def __init__(self):
		super().__init__()

	def startGame(self):
		super().startGame()
		self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) - 5), self.snakeSize*(self.grid[1]//2), "green",self.grid),
						 Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) + 5), self.snakeSize*(self.grid[1]//2), "blue",self.grid)]
		self.occupied[self.snakes[0].getPosition()] = [self.snakes[0].body[0].type]
		self.occupied[self.snakes[1].getPosition()] = [self.snakes[1].body[0].type]
		self.loop()

	def loop(self):
		if not(self.pause) and self.active:
			self.snakeAI(self.snakes,1)
			for snake in self.snakes:
				snake.move(self.occupied)
				if self.check(snake,self.food):
					snake.anotherOne()
					self.newFood()
				snake.commit = False
			oneLose = self.collide(self.snakes[0])
			twoLose = self.collide(self.snakes[1])
			if oneLose and twoLose:
				self.endTie()
			elif oneLose:
				self.end(self.snakes[1])
			elif twoLose:
				self.end(self.snakes[0])
			self.root.after(self.speed,self.loop)

	def endTie(self):
		self.active = False
		frame = Frame(self.root)
		message = ttk.Label(frame,text="It's a tie!!!",font="TkDefaultFont 48")
		restart = Button(frame,text = "Restart",command=self.startGame)
		menu = Button(frame,text = "Main Menu", command=self.snakeMenu)

		message.grid()
		restart.grid()
		menu.grid()

		self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

	def end(self,snake):
		self.active = False
		frame = Frame(self.root)
		message = ttk.Label(frame,text="The winner is "+snake.color+"!",font="TkDefaultFont 48")
		restart = Button(frame,text = "Restart",command=self.startGame)
		menu = Button(frame,text = "Main Menu", command=self.snakeMenu)

		message.grid()
		restart.grid()
		menu.grid()

		self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

	def snakeAI(self,snakelist,mySnake):
		myself = snakelist[mySnake]
		difference = (self.food.getPosition()[0] - snakelist[mySnake].getPosition()[0],
					  self.food.getPosition()[1] - snakelist[mySnake].getPosition()[1])
		if difference[0] > 0:
			snakelist[mySnake].goRight()
		elif difference[0] < 0:
			snakelist[mySnake].goLeft()
		elif difference[1] > 0:
			snakelist[mySnake].goDown()
		else:
			snakelist[mySnake].goUp()
