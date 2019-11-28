"""
Abby Nason
smash! the ceiling
main.py

TODO by end of Thanksgiving:

make main shorter:
    - move everything to level manager

forcefield:
    - follows the blob: completed
    - make drawing of forcefield and collision box bigger
    - need to create a new drawing

levels:
    - completed: different color schemes for different levels
    - one more level with original blob (vertical that goes to ceiling)
    - one level with one of the other blobs
    - not started

boss enemy:
    - character that spawns mini blobs
    - have to avoid hitting the blobs: takes down wokeness meter or something like that

smash animation:
    - running toward trying to smash the ceiling unsuccessful
    - animation that shows that you have to train other blobs

menus:
    - start menu
    - blob selection screen:
        - three other blobs to select from
        - once you click on one it takes you to next level with one of the blobs


cheats to go to end of level:
    - cheat codes

music and sound effects:
    - background music: the man by taylor swift, nightmare by halsey if possible

make screen bigger for demo:
    - upscale
"""



import pygame
import os
from modules.vector2D import Vector2
import random
from characters.orb import Orb
from characters.blob import Blob
from characters.bra import Bra
from characters.pan import Pan
from characters.ring import Ring
from characters.elevator import Elevator
from modules.drawable import Drawable
from modules.level_parser import LevelParser
#from modules.gameManager import GameManager

# screen size is the amount we show the player
# world size is the size of the interactable world
SCREEN_SIZE = (400, 400)
WORLD_SIZE = (2400, 400)
CHAR_SPRITE_SIZE = Vector2(32, 32)
LEVELS = ["level1.txt", "level2.txt", "level3.txt"]
LEVELS_IN_PROGRESS = ["level4.txt"]
MENUS = ["startmenu.txt", "blobmenu.txt"]
ANIMATIONS = ["smash1.txt", "smash2.txt"]
ORDER = {1: (MENUS, 0), 2:(LEVELS, 0), 3:(LEVELS, 1), 4: (LEVELS, 2), 5: (ANIMATIONS, 0), 6:(MENUS, 1), 7:(LEVELS, 3), 8:(ANIMATIONS, 1)}

def main():

   # initialize the pygame module
   pygame.init()

   # load and set the logo
   pygame.display.set_caption("Smash! the Ceiling")

   # creating the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   platforms = []
   traps = []

   level = LevelParser(LEVELS[0])
   level.loadLevel()
   WORLD_SIZE = level._worldsize

   #background = Drawable("background.png", Vector2(0,0), (0,0))
   #ground = Drawable("ground2.png", Vector2(0, 300), (0,0))

   # initialize the blob on top of the ground
   #blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))

   #elevator = Elevator(Vector2(WORLD_SIZE[0]-50,300), WORLD_SIZE[1])

   nextLevel = 1

   # initialize the orb list
   #orbs = []

   # set the offset of the window into the world
   offset = Vector2(0,0)

   # initialize the game clock
   gameClock = pygame.time.Clock()

   # define a variable to control the main loop
   RUNNING = True

   endCount = 0

   # main loop
   while RUNNING:

      gameClock.tick()

      #RESOLUTION = [400, 400]
      #SCALE = 3
      #UPSCALED = [x * SCALE for x in RESOLUTION]

      #screen = pygame.display.set_mode(UPSCALED)
      #drawSurface = pygame.Surface(RESOLUTION)

      #drawSurface.fill((255,255,255))
     # pygame.draw.circle(drawSurface, <etc>)
     # pygame.transform.scale(drawSurface,  UPSCALED, screen)



      # draw everything based on the offset
      #screen.blit(background, (-offset[0], -offset[1]))
      level.draw(screen)

      # flip display to the monitor
      pygame.display.flip()

      level.detectCollision()


      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # handle arrow key up and down events
         else:
             level.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000
      level.update(WORLD_SIZE, SCREEN_SIZE, ticks)

      for door3 in level._elevator._parts["back"]:
          clipper = level._blob.getCollideRect().clip(door3.getCollideRect())
          if level._blob._FSM == "grounded" and clipper.width == 32:
              endCount += 1
              level._blob.handleEndLevel()
              #print(blob._position)
          #elif endCount > 30:
              if level._blob._position.y < 0:
                  level = LevelParser(LEVELS[nextLevel])
                  nextLevel += 1
                  if nextLevel > len(LEVELS) - 1:
                      nextLevel = 0
                  level.loadLevel()
                  WORLD_SIZE = level._worldsize
                  level._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y),level._blob._color)

if __name__ == "__main__":
   main()
