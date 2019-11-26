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
    - different color schemes for different levels
    - one more level with original blob (vertical that goes to cieling)
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
LEVELS = ["level1.txt", "level2.txt"]

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

   deathCycle = 0

   endCount = 0

   # main loop
   while RUNNING:

      gameClock.tick()

      # draw everything based on the offset
      #screen.blit(background, (-offset[0], -offset[1]))
      level.draw(screen)

      for category3 in level._traps:
          for trap3 in level._traps[category3]:
              if trap3.ranInto():
                  if category3 == "bra":
                      level._traps[category3].remove(trap3)
                  elif category3 == "pan":
                      trap3.resetRanInto()
      # flip display to the monitor
      pygame.display.flip()

      clipRect = level._blob.getCollideRect().clip(level._ground.getCollideRect())

      if clipRect.width > 0:
         level._blob.manageState("collideGround")

      #variable to determine if already collided with a platform
      i = True
      blobPos = level._blob.getCollideRect()
      totalClipWidth = 0
      for platform in level._platforms:
          platPos = platform.getCollideRect()
          clipRect2 = blobPos.clip(platPos)
          totalClipWidth += clipRect2.width
          if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
              if blobPos[0] < platPos[0] and level._blob._velocity.x >= 0:
                  if level._blob._velocity.x == 0:
                      level._blob._velocity.x = -100
                  else:
                      level._blob._velocity.x = -level._blob._velocity.x
              elif blobPos[0] + blobPos[2] > platPos[0] + platPos[2] and level._blob._velocity.x <= 0:
                  if level._blob._velocity.x == 0:
                      level._blob._velocity.x = 100
                  else:
                      level._blob._velocity.x = -level._blob._velocity.x
              if level._blob._velocity.y <= 0:
                  level._blob._velocity.y = -level._blob._velocity.y
              level._blob.manageState("fall")
          elif (clipRect2.width >= 5 or (clipRect2.width > 0 and totalClipWidth == 32)) and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
              level._blob.manageState("collidePlatform")
              i = False
          elif clipRect2.width < 5 and level._blob._FSM == "platformed" and i:
              level._blob.manageState("fall")
              level._blob.updateVisual()

      for category in level._traps:
          for trap in level._traps[category]:
              if level._blob.getCollideRect().colliderect(trap.getCollideRect()):
                  trap.handleCollision()
                  if category == "bra":
                      level._blob._velocity.x = -level._blob._velocity.x
                      if not level._blob._forcefield.isActive():
                          level._blob.die()
                  elif category == "pan":
                      level._blob._velocity.x = -level._blob._velocity.x * 0.5
                      level._blob._velocity.y = -level._blob._velocity.y
                      if not level._blob._forcefield.isActive():
                          level._blob.die()
                  elif category == "ring":
                      if blobPos[0] + blobPos[2] > trap.getCollideRect()[0] + trap.getCollideRect()[2]:
                          level._blob._velocity.x = 100
                      else:
                          level._blob._velocity.x = -100
                      level._blob._velocity.y = -level._blob._velocity.y

      for category4 in level._traps:
          for trap4 in level._traps[category4]:
              for zap4 in level._blob._zaps:
                  if zap4.getCollideRect().colliderect(trap4.getCollideRect()):
                      if category4 == "bra":
                          trap4.handleCollision()
                          zap4.handleDestroy()
                      if category4 == "pan":
                          level._traps[category4].remove(trap4)
                          zap4.handleDestroy()
                      elif category4 == "ring":
                           zap4.handleEnd()

      for category17 in level._enemies:
          for enemy17 in level._enemies[category17]:
              for zap17 in level._blob._zaps:
                  if zap17.getCollideRect().colliderect(enemy17.getCollideRect()):
                      enemy17.handleCollision()
                      #print(enemy17._hp)
                      zap17.handleDestroy()
                      if enemy17.isDead() and enemy17 in level._enemies[category17]:
                          level._enemies[category17].remove(enemy17)

      for category21 in level._enemies:
          for enemy21 in level._enemies[category21]:
              if level._blob.getCollideRect().colliderect(enemy21.getCollideRect()):
                  level._blob._velocity.x = -level._blob._velocity.x
                  if category21 == "devil":
                      if not level._blob._forcefield.isActive():
                          level._blob.die()

      for ring7 in level._traps["ring"]:
          for ringZap in ring7._zaps:
              for blobZap in level._blob._zaps:
                  if ringZap.getCollideRect().colliderect(blobZap.getCollideRect()):
                      ringZap.handleDestroy()
                      blobZap.handleDestroy()

      for gaston50 in level._enemies["gaston"]:
          for arrow50 in gaston50._arrows:
              for blobZap50 in level._blob._zaps:
                  if arrow50.getCollideRect().colliderect(blobZap50.getCollideRect()):
                      arrow50.handleDestroy()
                      blobZap50.handleDestroy()

      if level._blob._forcefield.isActive():
          for ring40 in level._traps["ring"]:
              for ringZap40 in ring40._zaps:
                  if ringZap40.getCollideRect().colliderect(level._blob._forcefield.getCollideRect()):
                      ringZap40.handleDestroy()

          for gaston82 in level._enemies["gaston"]:
              for arrow82 in gaston82._arrows:
                  if arrow82.getCollideRect().colliderect(level._blob._forcefield.getCollideRect()):
                      arrow82.handleDestroy()

      for ring20 in level._traps["ring"]:
          for zap20 in ring20._zaps:
              if zap20.getCollideRect().colliderect(level._blob.getCollideRect()):
                  zap20.handleDestroy()
                  if not level._blob._forcefield.isActive():
                      level._blob.die()

      for gaston64 in level._enemies["gaston"]:
          for arrow64 in gaston64._arrows:
              if arrow64.getCollideRect().colliderect(level._blob.getCollideRect()):
                  arrow64.handleDestroy()
                  if not level._blob._forcefield.isActive():
                      level._blob.die()

      for door in level._elevator._parts["doors"]:
          for zap102 in level._blob._zaps:
              if zap102.getCollideRect().colliderect(door.getCollideRect()):
                  zap102.handleEnd()

      for platform3 in level._platforms:
          for zap5 in level._blob._zaps:
              if zap5.getCollideRect().colliderect(platform3.getCollideRect()):
                  zap5.handleEnd()
          for ring15 in level._traps["ring"]:
              for zap15 in ring15._zaps:
                  if zap15.getCollideRect().colliderect(platform3.getCollideRect()):
                      zap15.handleEnd()
                  #blob._zaps.remove(zap5)


      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # handle arrow key up and down events
         else:
             level._blob.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000
      level._blob.update(WORLD_SIZE, ticks)
      for pan in level._traps["pan"]:
          pan.update(ticks)
      for zap2 in level._blob._zaps:
          zap2.update(WORLD_SIZE, ticks)
      for devil in level._enemies["devil"]:
          devil.update(WORLD_SIZE, ticks)
      for gaston in level._enemies["gaston"]:
          gaston.update(WORLD_SIZE, ticks)
      for ring in level._traps["ring"]:
          ring.update(WORLD_SIZE, ticks)

      if level._blob.isDead():
          #print(deathCycle)
          if deathCycle > 30:
              level.reset()
              level.loadLevel()
              # initialize the blob on top of the ground
              level._blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))
              deathCycle = 0
          deathCycle += 1

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
                  level._blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))



      # getting the offset of the of the star (our tracking object)
      Drawable.updateOffset(level._blob, SCREEN_SIZE, WORLD_SIZE)

if __name__ == "__main__":
   main()
