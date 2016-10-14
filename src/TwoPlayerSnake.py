# TwoPlayerSnake class which is a two player version of the base SnakeGame

#TODO: combine endTie and end into one

from SnakeGame import *

class TwoPlayerSnake(SnakeGame):
	def __init__(self):
		super().__init__()

	def startGame(self):
		super().startGame()
		# additional bindings for player 2   
		self.root.bind("<Left>",self.goLeft)
		self.root.bind("<Up>",self.goUp)
		self.root.bind("<Down>",self.goDown)
		self.root.bind("<Right>",self.goRight)
		# add two snakes, one for each player
		self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) - 5), self.snakeSize*(self.grid[1]//2), "green",self.grid),
						 Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) + 5), self.snakeSize*(self.grid[1]//2), "blue",self.grid)]
		# start game loop
		self.loop()

	def loop(self):
		# make sure game is still going
		if not(self.pause) and self.active:
			# move all the snakes
			for snake in self.snakes:
				snake.move()
				if self.check(snake,self.food):
					# snake ate food so grow it
					snake.anotherOne()
					# create new food
					self.newFood()
				# allow current snake to change direction again
				snake.commit = False
			# check for collisions
			oneLose = self.collide(self.snakes[0])
			twoLose = self.collide(self.snakes[1])
			if oneLose and twoLose:
				self.endTie()
			elif oneLose:
				self.end(self.snakes[1])
			elif twoLose:
				self.end(self.snakes[0])
			# restart loop after game speed
			self.root.after(self.speed,self.loop)

	def endTie(self):
		# stop game
		self.active = False
		# create information window
		frame = Frame(self.root)
		message = ttk.Label(frame,text="It's a tie!!!",font="TkDefaultFont 48")
		restart = Button(frame,text = "Restart",command=self.startGame)
		menu = Button(frame,text = "Main Menu", command=self.snakeMenu)
		message.grid()
		restart.grid()
		menu.grid()
		# put information window on game window
		self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

	def end(self,snake):
		# stop game
		self.active = False
		# create information window
		frame = Frame(self.root)
		message = ttk.Label(frame,text="The winner is "+snake.color+"!",font="TkDefaultFont 48")
		restart = Button(frame,text = "Restart",command=self.startGame)
		menu = Button(frame,text = "Main Menu", command=self.snakeMenu)
		message.grid()
		restart.grid()
		menu.grid()
		# put information window on game window
		self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)
