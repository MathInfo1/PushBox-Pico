# PushBox-Pico
Cool grid game, can be played with ILI9488 display and microcontrollers supporting MicroPython

For the installation and circuit, read the release. 

How to play: 
- The green circle on the top left is the player.
- The orange squares are the boxes.
- The black squares are the fields to push the boxes.
- Controls: Lift 1 of the 4 input pins to move in a specific direction.
- You can push only 1 box at a time.
- If a box is stuck at the edge, move it to the blue jumper pads, the box gets pushed diagonally.
- Once you push all 5 boxes in the goal, you get a winning animation showing your score in binary (white = 0, black = 1). 10sec later the game restarts itself.
- Enjoy (and good luck with the controls :) They aren't that hard to learn)!

Detailed controls:
- lift pin 4: go right
- lift pin 5: go left
- lift pin 6: go down
- lift pin 7: go up
- you can't move diagonally

