from my_display import *
from random import randint

class PushBox():
    def __init__(self, display, moveInput, gridSize):
        self.display = display
        self.input = moveInput
        self.gridSize = gridSize
        self.createGrid()

    def createGrid(self):
        self.grid = [[0 for j in range(self.display.screenSize[1] // self.gridSize)] for i in range(self.display.screenSize[0] // self.gridSize)]
        self.pos = (-1, -1)
        self.drawFullScreen()
        self.pos = (0, 0)
        self.drawPlayer(self.pos[0], self.pos[1])

    def addBoxAndField(self, numBoxes=1):
        for i in range(numBoxes):
            pos = (randint(0, self.display.screenSize[0] // self.gridSize - 1), randint(0, self.display.screenSize[1] // self.gridSize - 1))
            while self.grid[pos[0]][pos[1]] != 0:
                pos = (randint(0, self.display.screenSize[0] // self.gridSize - 1), randint(0, self.display.screenSize[1] // self.gridSize - 1))
            self.grid[pos[0]][pos[1]] = 2
            self.drawBox(pos[0], pos[1])

            pos = (randint(0, self.display.screenSize[0] // self.gridSize - 1), randint(0, self.display.screenSize[1] // self.gridSize - 1))
            while self.grid[pos[0]][pos[1]] != 0:
                pos = (randint(0, self.display.screenSize[0] // self.gridSize - 1), randint(0, self.display.screenSize[1] // self.gridSize - 1))
            self.grid[pos[0]][pos[1]] = 3
            self.drawGoal(pos[0], pos[1])

    def drawFullScreen(self):
        for i in range(self.display.screenSize[0] // self.gridSize):
            for j in range(self.display.screenSize[1] // self.gridSize):
                if self.pos == (i, j):
                    self.drawPlayer(i, j)
                else:
                    self.drawField(i, j)
    
    def drawPlayer(self, x, y):
        # self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (0, 255, 0))
        self.display.drawCircle((x + 0.5) * self.gridSize, (y + 0.5) * self.gridSize, 20, (255, 0, 0))

    def drawBox(self, x, y):
        self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (252, 136, 24))

    def drawGoal(self, x, y):
        self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (0, 0, 5))
        
    def drawFloor(self, x, y):
        if (x + y) % 2 == 0:
            self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (200, 200, 200))
        else: 
            self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (64, 64, 64))
            
    def drawField(self, x, y):
        if self.grid[x][y] == 0:
            self.drawFloor(x, y)
        elif self.grid[x][y] == 2:
            self.drawBox(x, y)
        elif self.grid[x][y] == 3:
            self.drawGoal(x, y)
        
    def move(self, x, y):
        if (x, y) != (0, 0) and 0 <= self.pos[0] + x < self.display.screenSize[0] // self.gridSize and 0 <= self.pos[1] + y < self.display.screenSize[1] // self.gridSize:
            self.drawField(self.pos[0], self.pos[1])
            print(self.grid[self.pos[0]][self.pos[1]])
            self.pos = (self.pos[0] + x, self.pos[1] + y)
            self.drawPlayer(self.pos[0], self.pos[1])

