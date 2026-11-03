from push_box import *
from my_display import * 
from my_input import *
from random import randint
from time import sleep_ms

myDisplay = Display(18, 19, 16, 17, 22, 21, 13, "landscape")
myInput = Input(7, 4, 6, 5)

# Please play this game in landscape mode, there can be problems with portrait mode
myGame = PushBox(myDisplay, myInput, 40)
myGame.addBoxAndField(5)
print(myGame.grid)


while True:
    move = myInput.getDirection()
    myGame.move(move[0], move[1])
    if move != (0, 0): print(move)
    sleep_ms(500)

