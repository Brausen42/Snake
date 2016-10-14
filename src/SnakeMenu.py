# SnakeMenu class for starting an appropriate SnakeGame

from Window import *
from SinglePlayerSnake import *
from TwoPlayerSnake import *
from PlayerVsAISnake import *

class SnakeMenu(Window):
	def __init__(self):
		super().__init__()
		self.root.title = "Snake"
		self.createMainScreen()
		# allow root window to read input
		self.root.mainloop()
		
		
	def createMainScreen(self):
		# reset window
		self.clearWindow()
		# configure root window
		self.root.columnconfigure(0,weight = 1)
		buttonQuantity = 3
		# generate button text style
		BUTTONS = "TkDefaultFont " + str(self.size[1] // (2*(buttonQuantity + 3)))
		snakeTitle = ttk.Label(self.root,text="Snake",font="TkHeadingFont " + str(2*(self.size[1] // (2*(buttonQuantity + 3)))) ,anchor=N)
		snakeTitle.grid(column = 0,row = 0)
		# create all buttons
		onePlayer = Button(self.root,text="Classic",font=BUTTONS ,command=self.singlePlayer)
		onePlayer.grid(column = 0, row = 1)
		twoPlayer = Button(self.root,text="Versus",font=BUTTONS ,command=self.versus)
		twoPlayer.grid(column = 0, row = 2)
		settings = Button(self.root,text="Exit",font=BUTTONS, command=self.exit)
		settings.grid(column = 0, row = 3)


	def versus(self):
		# reset window
		self.clearWindow()
		# configure root window
		self.root.columnconfigure(0,weight = 1)
		buttonQuantity = 3
		# generate button text style
		BUTTONS = "TkDefaultFont " + str(self.size[1] // (2*(buttonQuantity + 3)))
		snakeTitle = ttk.Label(self.root,text="Versus",font="TkHeadingFont " + str(2*(self.size[1] // (2*(buttonQuantity + 3)))),anchor=N)
		snakeTitle.grid(column = 0,row = 0)
		# create all buttons
		onePlayer = Button(self.root,text="Player vs. Player",font=BUTTONS ,command=self.twoPlayer)
		onePlayer.grid(column = 0, row = 1)
		twoPlayer = Button(self.root,text="Player vs. Computer",font=BUTTONS ,command=self.vsAI)
		twoPlayer.grid(column = 0, row = 2)
		settings = Button(self.root,text="Back",font=BUTTONS, command=self.createMainScreen)
		settings.grid(column = 0, row = 3)

	# methods for starting a particular game after closing the snake menu
	def singlePlayer(self):
		self.exit()
		SinglePlayerSnake()

	def twoPlayer(self):
		self.exit()
		TwoPlayerSnake()

	def vsAI(self):
		self.exit()
		PlayerVsAISnake()
