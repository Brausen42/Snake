from Unit import *

class Snake:
            
    def __init__(self,master,size,x,y,color,grid):
        self.length = 1
        self.another = False
        self.pieceSize = size
        self.color = color
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.direction = ""
        self.commit = False
        self.master = master
        self.grid = (grid[0] + 1,grid[1] + 1)
        self.body = [Unit(master,size,x,y,color)]

    def goUp(self):
        self.direction = "UP"
        self.xVel = 0
        self.yVel = -1

    def goDown(self):
        self.direction = "DOWN"
        self.xVel = 0
        self.yVel = 1

    def goLeft(self):
        self.direction = "LEFT"
        self.xVel = -1
        self.yVel = 0

    def goRight(self):
        self.direction = "RIGHT"
        self.xVel = 1
        self.yVel = 0

    def move(self):
        tempY = self.y + (self.yVel*self.pieceSize)
        self.y = tempY % (self.grid[1]*self.pieceSize)
        tempX = self.x + (self.xVel*self.pieceSize)
        self.x = tempX % (self.grid[0]*self.pieceSize)

        
        temp = self.body.pop()
        pos = temp.getPosition()
        x = pos[0]
        y = pos[1]
        temp.move((self.x, self.y))
        
        self.body.insert(0,temp)
        if self.another:
            self.body.append(Unit(self.master,self.pieceSize,x,y, self.color))
            self.another = False
            
        return ((tempX == self.x) and (tempY == self.y))

    def anotherOne(self):
        self.another = True
        self.length += 1

    def getPosition(self):
        return (self.x,self.y)

    def getPositionList(self):
        returnList = []
        for piece in self.body:
            returnList.append(piece.getPosition())
        return returnList
