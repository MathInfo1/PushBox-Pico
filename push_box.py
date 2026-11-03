from my_display import *
from random import randint
from time import sleep_ms

class PushBox():
    def __init__(self, display, moveInput, gridSize):
        self.display = display
        self.input = moveInput
        self.gridSize = gridSize
        self.numCol = self.display.screenSize[0] // self.gridSize
        self.numRow = self.display.screenSize[1] // self.gridSize
        self.gameStatus = -1
        self.createGrid()

    def createGrid(self):
        self.moves = 0
        self.numBoxes = 0
        self.boxesRemaining = 0
        self.grid = [[0 for j in range(self.numRow)] for i in range(self.numCol)]
        self.pos = (-1, -1)
        self.grid[0][0] = 1
        self.grid[0][self.numRow - 1] = 1
        self.grid[self.numCol - 1][0] = 1
        self.grid[self.numCol - 1][self.numRow - 1] = 1
        self.drawFullScreen()
        self.pos = (0, 0)
        self.drawPlayer(self.pos[0], self.pos[1])

    def addBoxAndField(self, numBoxes=1):
        for i in range(numBoxes):
            pos = (randint(0, self.numCol - 1), randint(0, self.numRow - 1))
            while self.grid[pos[0]][pos[1]] != 0:
                pos = (randint(0, self.numCol - 1), randint(0, self.numRow - 1))
            self.grid[pos[0]][pos[1]] = 2
            self.drawBox(pos[0], pos[1])

            pos = (randint(0, self.numCol - 1), randint(0, self.numRow - 1))
            while self.grid[pos[0]][pos[1]] != 0 or pos in [(0, 0), (0, self.numRow - 1), (self.numCol - 1, 0), (self.numCol - 1, self.numRow - 1)]:
                pos = (randint(0, self.numCol - 1), randint(0, self.numRow - 1))
            self.grid[pos[0]][pos[1]] = 3
            self.drawGoal(pos[0], pos[1])
        self.boxesRemaining += numBoxes
        self.numBoxes += numBoxes
        self.gameStatus = 0

    def drawFullScreen(self):
        for i in range(self.numCol):
            for j in range(self.numRow):
                if self.pos == (i, j):
                    self.drawPlayer(i, j)
                else:
                    self.drawField(i, j)
    
    def drawPlayer(self, x, y):
        # self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (0, 255, 0))
        self.display.drawCircle((x + 0.5) * self.gridSize, (y + 0.5) * self.gridSize, 20, (0, 255, 0))

    def drawBox(self, x, y):
        self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (252, 136, 24))

    def drawGoal(self, x, y):
        self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (0, 0, 5))
        
    def drawFloor(self, x, y):
        if (x + y) % 2 == 0:
            self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (200, 200, 200))
        else: 
            self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (64, 64, 64))
    
    def drawJumpPad(self, x, y):
        self.display.drawRect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize, (0, 0, 255))
    
    def drawField(self, x, y):
        if self.grid[x][y] == 0:
            self.drawFloor(x, y)
        elif self.grid[x][y] == 1:
            self.drawJumpPad(x, y)
        elif self.grid[x][y] == 2:
            self.drawBox(x, y)
        elif self.grid[x][y] == 3:
            self.drawGoal(x, y)
        
    def move(self, x, y):
        if abs(x + y) == 1 and (x, y) != (0, 0) and 0 <= self.pos[0] + x < self.numCol and 0 <= self.pos[1] + y < self.numRow:
            newPos = (self.pos[0] + x, self.pos[1] + y)
            if self.grid[newPos[0]][newPos[1]] != 2:
                self.moves += 1
                self.drawField(self.pos[0], self.pos[1])
                print(self.grid[self.pos[0]][self.pos[1]])
                self.pos = newPos
                self.drawPlayer(self.pos[0], self.pos[1])
                return 
            if self.grid[newPos[0]][newPos[1]] == 2:
                if 0 <= self.pos[0] + 2 * x < self.numCol and 0 <= self.pos[1] + 2 * y < self.numRow:
                    n2Pos = (self.pos[0] + 2 * x, self.pos[1] + 2 * y)
                    if self.grid[n2Pos[0]][n2Pos[1]] != 2:
                        self.moves += 1
                        self.drawField(self.pos[0], self.pos[1])
                        self.grid[newPos[0]][newPos[1]] = 0
                        self.drawField(newPos[0], newPos[1])
                        if self.grid[n2Pos[0]][n2Pos[1]] == 3:
                            self.grid[n2Pos[0]][n2Pos[1]] = 0
                            self.boxesRemaining -= 1
                            print(self.gameStatus, self.boxesRemaining)
                            if self.gameStatus == 0 and self.boxesRemaining == 0:
                                self.gameWon()
                                return
                        elif self.grid[n2Pos[0]][n2Pos[1]] == 0:
                            self.grid[n2Pos[0]][n2Pos[1]] = 2
                        elif self.grid[n2Pos[0]][n2Pos[1]] == 1:
                            jumpPos = (1 if n2Pos[0] == 0 else self.numCol - 2, 1 if n2Pos[1] == 0 else self.numRow - 2)
                            self.grid[jumpPos[0]][jumpPos[1]] = 2
                            self.drawField(jumpPos[0], jumpPos[1])
                        self.drawField(n2Pos[0], n2Pos[1])
                        print(self.grid[self.pos[0]][self.pos[1]])
                        self.pos = newPos
                        self.drawPlayer(self.pos[0], self.pos[1])

    def gameWon(self):
        # Winning animation
        print(self.moves)
        for i in range(self.numCol):
            for j in range(self.numRow):
                self.display.drawRect(i * self.gridSize, j * self.gridSize, self.gridSize, self.gridSize, (randint(0, 20), randint(232, 255), randint(0, 20)))
                sleep_ms(20)
                
        # Draw score in binary :D
        for i in range(self.numCol - 2):
            if self.moves & 2 ** i != 0:
                self.display.drawRect((self.numCol - 2 - i) * self.gridSize, self.gridSize, self.gridSize, self.gridSize, (0, 0, 0))
            else:
                self.display.drawRect((self.numCol - 2 - i) * self.gridSize, self.gridSize, self.gridSize, self.gridSize, (255, 255, 255))
        # Restart game
        sleep_ms(10000)
        numBoxes = self.numBoxes
        self.createGrid()
        self.addBoxAndField(numBoxes)
