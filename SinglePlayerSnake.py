from SnakeGame import *
from Mine import *

class SinglePlayerSnake(SnakeGame):
    def __init__(self):
        super().__init__()

    def startGame(self):
        super().startGame()

        self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), "green",self.grid)]
        
        self.mines = []
        
        self.loop()

    def loop(self):
        if not(self.pause) and self.active:
            if (not self.snakes[0].move()) or self.checkMine(self.mines):
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

    def newFood(self):
        self.speed = math.ceil(self.speed * .98)
        self.food.destroy()
        bad = True
        while bad:
            bad = False
            xpos = self.snakeSize*random.randint(0,self.grid[0])
            ypos = self.snakeSize*random.randint(0,self.grid[1])
            for mine in self.mines:
                if mine.getPosition == (xpos,ypos):
                    bad = True
            for snake in self.snakes:
                if (xpos,ypos) in snake.getPositionList():
                    bad = True
                
        self.food = Food(self.canvas,self.snakeSize,xpos,ypos,"yellow")

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

    def checkMine(self,mines):
        for mine in mines:
            for snake in self.snakes:
                if snake.getPosition() == mine.getPosition():
                    return True
