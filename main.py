"""
Abby Nason
smash! the ceiling
main.py

Controls the progress of the game
"""



import pygame
import os
from modules.vector2D import Vector2
import random
from characters.blob import Blob
from characters.bra import Bra
from characters.pan import Pan
from characters.ring import Ring
from characters.elevator import Elevator
from modules.drawable import Drawable
from modules.level_parser import LevelParser
from modules.menu_parser import MenuParser
from modules.animation_parser import AnimationParser
from modules.soundManager import SoundManager

# screen size is the amount we show the player
# world size is the size of the interactable world
SCREEN_SIZE = [400, 400]
WORLD_SIZE = (2400, 400)
SCALE = 2
UPSCALED = [x * SCALE for x in SCREEN_SIZE]
CHAR_SPRITE_SIZE = Vector2(32, 32)

#keeping track of the order of levels, animations, and menus
LEVELS = ["level1.txt", "level2.txt", "level3.txt", "level4.txt", "level5.txt", "level6.txt"]
MENUS = ["startmenu.txt", "blobmenu.txt"]
ANIMATIONS = ["smash1.txt", "smash2.txt"]
ORDER = {1: (MENUS, 0), 2:(LEVELS, 0), 3:(LEVELS, 1), 4: (LEVELS, 2), 5:(LEVELS, 4), 6: (ANIMATIONS, 0), 7:(MENUS, 1), 8:(LEVELS, 3), 9:(LEVELS, 5), 10:(ANIMATIONS,1)}

def main():

   # initialize the pygame module
   pygame.init()

   # load and set the logo
   pygame.display.set_caption("Smash! the Ceiling")

   # creating the screen
   #screen = pygame.display.set_mode(SCREEN_SIZE)
   screen = pygame.display.set_mode(UPSCALED)
   drawSurface = pygame.Surface(SCREEN_SIZE)

   platforms = []
   traps = []

   nextPhase = 1

   phase = ORDER[nextPhase]

   #load the first phase
   if phase[0] == LEVELS:
       level = LevelParser(phase[0][phase[1]])
       level.loadLevel()
   elif phase[0] == MENUS:
       level = MenuParser(phase[0][phase[1]])
       level.loadMenu()
   elif phase[0] == ANIMATIONS:
       level = AnimationParser(phase[0][phase[1]])
       level.loadAnimation()
   #elif phase[0] = ANIMATIONS:

   WORLD_SIZE = level._worldsize

   nextPhase += 1

   # initialize the orb list
   #orbs = []

   # set the offset of the window into the world
   offset = Vector2(0,0)

   # initialize the game clock
   gameClock = pygame.time.Clock()

   # define a variable to control the main loop
   RUNNING = True

   endCount = 0

   #play music
   SoundManager.getInstance().playMusic("TheMan.ogg", loop=-1)

   # main loop
   while RUNNING:

      gameClock.tick()

      # draw everything based on the offset and upscale
      if phase[0] == LEVELS:
          level.draw(drawSurface)
          pygame.transform.scale(drawSurface,UPSCALED,screen)
      elif phase[0] == MENUS:
          level.draw(drawSurface)
          pygame.transform.scale(drawSurface,UPSCALED,screen)
      elif phase[0] == ANIMATIONS:
          level.draw(drawSurface)
          pygame.transform.scale(drawSurface,UPSCALED,screen)

      # flip display to the monitor
      pygame.display.flip()

      if phase[0] == LEVELS:
          level.detectCollision()


      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # handle events in the level or menu
         else:
             if phase[0] == LEVELS:
                 level.handleEvent(event)
             if phase[0] == MENUS:
                 level.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000

      #checking if it's time to transition to next phase from a level
      if phase[0] == LEVELS:
          level.update(WORLD_SIZE, SCREEN_SIZE, ticks)

          #if level 1, 2, or 4
          if phase[0][phase[1]] != "level3.txt" and phase[0][phase[1]] != "level5.txt" and phase[0][phase[1]] != "level6.txt":
              #if in an elevator
              for door3 in level._elevator._parts["back"]:
                  clipper = level._blob.getCollideRect().clip(door3.getCollideRect())
                  if level._blob._FSM == "grounded" and clipper.width == 32:
                      level._blob.handleEndLevel()
                      if level._blob._position.y < 0:
                          phase = ORDER[nextPhase]
                          if phase[0] == LEVELS:
                              #if level is next
                              level = LevelParser(phase[0][phase[1]])
                              level.loadLevel()
                              WORLD_SIZE = level._worldsize
                              if level._filename != "level6.txt":
                                  level._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y),level._blob._color)
                          elif phase[0] == MENUS:
                              #if menu is next
                              level = MenuParser(phase[0][phase[1]])
                              level.loadMenu()
                              WORLD_SIZE = level._worldsize
                          elif phase[0] == ANIMATIONS:
                              #if animation is next
                              level = AnimationParser(phase[0][phase[1]])
                              level.loadAnimation()
                              WORLD_SIZE = level._worldsize
                          nextPhase += 1
                          if nextPhase > len(ORDER):
                              nextPhase = 1

          #if level 3 or 6
          elif phase[0][phase[1]] == "level3.txt" or phase[0][phase[1]] == "level6.txt":
              #if hit the ceiling the right number of times
              if level._ceiling.readyForNextLevel():
                  endCount += 1
                  if endCount > 150:
                      phase = ORDER[nextPhase]
                      endCount = 0
                      if phase[0] == LEVELS:
                          #if level is next
                          level = LevelParser(phase[0][phase[1]])
                          level.loadLevel()
                          WORLD_SIZE = level._worldsize
                          if level._filename != "level6.txt":
                              level._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y),level._blob._color)
                      elif phase[0] == MENUS:
                          #if menu is next
                          level = MenuParser(phase[0][phase[1]])
                          level.loadMenu()
                          WORLD_SIZE = level._worldsize
                      elif phase[0] == ANIMATIONS:
                          #if animation is next
                          level = AnimationParser(phase[0][phase[1]])
                          level.loadAnimation()
                          WORLD_SIZE = level._worldsize
                      nextPhase += 1
                      if nextPhase > len(ORDER):
                          nextPhase = 1
          #if level 5
          elif phase[0][phase[1]] == "level5.txt":
                #if main blob has found the other blobs
                if level._blob._position.x > 250:
                    endCount += 1
                    if endCount > 100:
                        phase = ORDER[nextPhase]
                        if phase[0] == LEVELS:
                            #if level is next
                            level = LevelParser(phase[0][phase[1]])
                            level.loadLevel()
                            WORLD_SIZE = level._worldsize
                            if level._filename != "level6.txt":
                                level._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y),level._blob._color)
                        elif phase[0] == MENUS:
                            #if menu is next
                            level = MenuParser(phase[0][phase[1]])
                            level.loadMenu()
                            WORLD_SIZE = level._worldsize
                        elif phase[0] == ANIMATIONS:
                            #if animation is next
                            level = AnimationParser(phase[0][phase[1]])
                            level.loadAnimation()
                            WORLD_SIZE = level._worldsize
                        nextPhase += 1
                        if nextPhase > len(ORDER):
                            nextPhase = 1

      #checking if it's time to transition to next phase from a menu
      elif phase[0] == MENUS:
          #if selection made and ready for next level
          if level.madeSelection() and level.nextLevel():
              selection = level.getSelection()
              phase = ORDER[nextPhase]
              if phase[0] == LEVELS:
                  #if level is next
                  level = LevelParser(phase[0][phase[1]])
                  level.loadLevel()
                  if level._filename != "level6.txt":
                      level._blob = Blob(Vector2(0,level._worldsize[1]-100-CHAR_SPRITE_SIZE.y),color=selection)
              elif phase[0] == MENUS:
                  #if menu is next
                  level = MenuParser(phase[0][phase[1]])
                  level.loadMenu()
              elif phase[0] == ANIMATIONS:
                  #if animation is next
                  level = AnimationParser(phase[0][phase[1]])
                  level.loadAnimation()
              nextPhase += 1
              WORLD_SIZE = level._worldsize

      #checking if it's time to transition to next phase from an animation
      elif phase[0] == ANIMATIONS:
          level.update(ticks)
          if level.nextLevel():
              phase = ORDER[nextPhase]
              if phase[0] == LEVELS:
                  #if level is next
                  level = LevelParser(phase[0][phase[1]])
                  level.loadLevel()
                  if level._filename != "level6.txt":
                      level._blob = Blob(Vector2(0,level._worldsize[1]-100-CHAR_SPRITE_SIZE.y),color=selection)
              elif phase[0] == MENUS:
                  #if menu is next
                  level = MenuParser(phase[0][phase[1]])
                  level.loadMenu()
              elif phase[0] == ANIMATIONS:
                  #if animation is next
                  level = AnimationParser(phase[0][phase[1]])
                  level.loadAnimation()
              nextPhase += 1
              WORLD_SIZE = level._worldsize




if __name__ == "__main__":
   main()
