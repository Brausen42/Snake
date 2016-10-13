from SnakeGame import *

class TwoPlayerSnake(SnakeGame):
    def __init__(self):
        super().__init__()

    def startGame(self):

        super().startGame()        
        self.root.bind("<Left>",self.goLeft)
        self.root.bind("<Up>",self.goUp)
        self.root.bind("<Down>",self.goDown)
        self.root.bind("<Right>",self.goRight)
        self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) - 5), self.snakeSize*(self.grid[1]//2), "green",self.grid),
                         Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) + 5), self.snakeSize*(self.grid[1]//2), "blue",self.grid)]
        
        self.loop()

    def loop(self):
        if not(self.pause) and self.active:
            for snake in self.snakes:
                snake.move()
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
