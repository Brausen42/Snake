from tkinter import *
from tkinter import ttk
import random
import math


class Window:
    def __init__(self):
        self.full = True

        self.root = Tk()
        self.root.bind("<Escape>",self.toggleFull)
        self.root.attributes("-fullscreen",True)
        self.root.update()
        self.size = ((self.root.winfo_width()), (self.root.winfo_height()))
        
    def toggleFull(self,event):
        self.full = not(self.full)
        self.root.attributes("-fullscreen",self.full)

    def clearWindow(self):
        for child in self.root.grid_slaves():
            child.grid_forget()

    def exit(self):
        self.root.destroy()

class SnakeMenu(Window):
    def __init__(self):
        super().__init__()
        self.root.title = "Snake"
        self.createMainScreen()
        self.root.mainloop()
        
        
    def createMainScreen(self):
        self.clearWindow()
        self.root.columnconfigure(0,weight = 1)
        buttonQuantity = 3
        BUTTONS = "TkDefaultFont " + str(self.size[1] // (2*(buttonQuantity + 3)))
        snakeTitle = ttk.Label(self.root,text="Snake",font="TkHeadingFont " + str(2*(self.size[1] // (2*(buttonQuantity + 3)))) ,anchor=N)
        snakeTitle.grid(column = 0,row = 0)
        onePlayer = Button(self.root,text="Classic",font=BUTTONS ,command=self.singlePlayer)
        onePlayer.grid(column = 0, row = 1)
        twoPlayer = Button(self.root,text="Versus",font=BUTTONS ,command=self.versus)
        twoPlayer.grid(column = 0, row = 2)
        settings = Button(self.root,text="Exit",font=BUTTONS, command=self.exit)
        settings.grid(column = 0, row = 3)


    def versus(self):
        self.clearWindow()
        self.root.columnconfigure(0,weight = 1)
        buttonQuantity = 3
        BUTTONS = "TkDefaultFont " + str(self.size[1] // (2*(buttonQuantity + 3)))
        snakeTitle = ttk.Label(self.root,text="Versus",font="TkHeadingFont " + str(2*(self.size[1] // (2*(buttonQuantity + 3)))),anchor=N)
        snakeTitle.grid(column = 0,row = 0)
        onePlayer = Button(self.root,text="Player vs. Player",font=BUTTONS ,command=self.twoPlayer)
        onePlayer.grid(column = 0, row = 1)
        twoPlayer = Button(self.root,text="Player vs. Computer",font=BUTTONS ,command=self.vsAI)
        twoPlayer.grid(column = 0, row = 2)
        settings = Button(self.root,text="Back",font=BUTTONS, command=self.createMainScreen)
        settings.grid(column = 0, row = 3)

    def singlePlayer(self):
        self.exit()
        SinglePlayerSnake()

    def twoPlayer(self):
        self.exit()
        TwoPlayerSnake()

    def vsAI(self):
        self.exit()
        PlayerVsAISnake()


class SnakeGame(Window):
    def __init__(self):
        super().__init__()
        self.root.title = "Snake"
        self.snakeSize = 20
        self.root.update()
        self.grid = ((self.root.winfo_width()//self.snakeSize)-1, (self.root.winfo_height()//self.snakeSize)-1) 
        self.startGame()
        self.root.mainloop()
    
    def startGame(self):
        self.canvas = Canvas(self.root,
                             background = "black",
                             width = self.grid[0]*(self.snakeSize+1),
                             height = self.grid[1]*(self.snakeSize+1))
        self.canvas.grid(column = 0, row = 0, sticky=(N,S,E,W))

        self.root.bind("a",self.goLeft)
        self.root.bind("w",self.goUp)
        self.root.bind("s",self.goDown)
        self.root.bind("d",self.goRight)
        self.root.bind("<space>",self.pauseGame)

        self.food = Food(self.canvas,self.snakeSize,self.snakeSize*random.randint(0,self.grid[0]),self.snakeSize*random.randint(0,self.grid[1]),"yellow")

        self.active = True
        self.pause = False
        self.speed = 100

    
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
        for snake in self.snakes:
            if snake.getPosition() == second.getPosition():
                return True
    

    def newFood(self):
        self.speed = math.ceil(self.speed * .95)
        self.food.destroy()
        bad = True
        while bad:
            bad = False
            xpos = self.snakeSize*random.randint(0,self.grid[0])
            ypos = self.snakeSize*random.randint(0,self.grid[1])
            for snake in self.snakes:
                if (xpos,ypos) in snake.getPositionList():
                    bad = True
        self.food = Food(self.canvas,self.snakeSize,xpos,ypos,"yellow")

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
                snake.move()
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
        SnakeMenu()

   
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
        menu = Button(frame,text = "Main Menu", command=self.createMainScreen)
        
        message.grid()
        restart.grid()
        menu.grid()

        self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

    def end(self,snake):
        self.active = False
        frame = Frame(self.root)
        message = ttk.Label(frame,text="The winner is "+snake.color+"!",font="TkDefaultFont 48")
        restart = Button(frame,text = "Restart",command=self.startGame)
        menu = Button(frame,text = "Main Menu", command=self.createMainScreen)
        
        message.grid()
        restart.grid()
        menu.grid()

        self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

class PlayerVsAISnake(SnakeGame):
    def __init__(self):
        super().__init__()

    def startGame(self):
        super().startGame()
        self.snakes = [Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) - 5), self.snakeSize*(self.grid[1]//2), "green",self.grid),
                         Snake(self.canvas,self.snakeSize, self.snakeSize*((self.grid[0]//2) + 5), self.snakeSize*(self.grid[1]//2), "blue",self.grid)]

        self.loop()

    def loop(self):
        if not(self.pause) and self.active:
            self.snakeAI(self.snakes,1)
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
        menu = Button(frame,text = "Main Menu", command=self.createMainScreen)
        
        message.grid()
        restart.grid()
        menu.grid()

        self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

    def end(self,snake):
        self.active = False
        frame = Frame(self.root)
        message = ttk.Label(frame,text="The winner is "+snake.color+"!",font="TkDefaultFont 48")
        restart = Button(frame,text = "Restart",command=self.startGame)
        menu = Button(frame,text = "Main Menu", command=self.createMainScreen)
        
        message.grid()
        restart.grid()
        menu.grid()

        self.canvas.create_window(self.snakeSize*(self.grid[0]//2), self.snakeSize*(self.grid[1]//2), window=frame)

    def snakeAI(self,snakelist,mySnake):
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
            

class Unit:
    def __init__(self,master,size,x,y,color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.master = master
        self.create()

    def create(self):
        self.unit = self.master.create_rectangle(self.x,
                                       self.y,
                                       self.x+self.size,
                                       self.y+self.size,
                                       fill=self.color,
                                       width = 0)

    def move(self,location):
        x = location[0]
        y = location[1]
        self.master.delete(self.unit)
        self.unit = self.master.create_rectangle(x,y,x+self.size,y+self.size, fill = self.color, width = 0)
        self.x = x
        self.y = y

    def getPosition(self):
        return (self.x,self.y)

    def destroy(self):
        self.master.delete(self.unit)

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

class Food(Unit):
    def __init__(self,master,size,x,y,color):
        super().__init__(master,size,x,y,color)

    def create(self):
        self.unit = self.master.create_oval(self.x,
                                       self.y,
                                       self.x+self.size,
                                       self.y+self.size,
                                       fill=self.color,
                                       width = 0)

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


SnakeMenu()
