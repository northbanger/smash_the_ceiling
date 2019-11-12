"""
Abby Nason
smash! the ceiling
main.py

TODO by Friday:
gaston collision: completed
devil collision: completed
blob death: completed
elevator to transition to next level
forcefield
one level with one of the other blobs
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
from modules.drawable import Drawable
from modules.level_parser import LevelParser
#from modules.gameManager import GameManager

# screen size is the amount we show the player
# world size is the size of the interactable world
SCREEN_SIZE = (400, 400)
WORLD_SIZE = (2400, 400)
CHAR_SPRITE_SIZE = Vector2(32, 32)

def main():

   # initialize the pygame module
   pygame.init()

   # load and set the logo
   pygame.display.set_caption("Smash! the Ceiling")

   # creating the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   platforms = []
   traps = []

   background = Drawable("background.png", Vector2(0,0), (0,0))
   ground = Drawable("ground2.png", Vector2(0, 300), (0,0))

   level = LevelParser("level2.txt")
   level.loadLevel()

   # initialize the blob on top of the ground
   blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))

   # initialize the orb list
   #orbs = []

   # set the offset of the window into the world
   offset = Vector2(0,0)

   # initialize the game clock
   gameClock = pygame.time.Clock()

   # define a variable to control the main loop
   RUNNING = True

   deathCycle = 0

   # main loop
   while RUNNING:

      gameClock.tick()

      # draw everything based on the offset
      #screen.blit(background, (-offset[0], -offset[1]))
      background.draw(screen)
      ground.draw(screen)
      for decoration in level._decorations:
          decoration.draw(screen)
      for platform2 in level._platforms:
          platform2.draw(screen)
      for category2 in level._traps:
          for trap2 in level._traps[category2]:
              trap2.draw(screen)
      for category10 in level._enemies:
          for enemy10 in level._enemies[category10]:
              enemy10.draw(screen)
      blob.draw(screen)
      if blob._forcefield.isActive():
          blob._forcefield.draw(screen)
      for zap in blob._zaps:
          if zap.isActive():
              zap.draw(screen)
          elif zap.notActive() > 5:
              blob._zaps.remove(zap)
          else:
              zap.incNotActive()
              zap.draw(screen)
      for ringy in level._traps["ring"]:
          for zappy in ringy._zaps:
              if zappy.isActive():
                  zappy.draw(screen)
              elif zappy.notActive() > 5:
                  ringy._zaps.remove(zappy)
              else:
                  zappy.incNotActive()
                  zappy.draw(screen)
      for gas in level._enemies["gaston"]:
          for arrow15 in gas._arrows:
              if arrow15.isActive():
                  arrow15.draw(screen)
              elif zappy.notActive() > 5:
                  gas._arrows.remove(arrow15)
              else:
                  arrow15.incNotActive()
                  arrow15.draw(screen)

      for category3 in level._traps:
          for trap3 in level._traps[category3]:
              if trap3.ranInto():
                  if category3 == "bra":
                      level._traps[category3].remove(trap3)
                  elif category3 == "pan":
                      trap3.resetRanInto()
      # flip display to the monitor
      pygame.display.flip()

      clipRect = blob.getCollideRect().clip(ground.getCollideRect())

      if clipRect.width > 0:
         blob.manageState("collideGround")

      #variable to determine if already collided with a platform
      i = True
      blobPos = blob.getCollideRect()
      totalClipWidth = 0
      for platform in level._platforms:
          platPos = platform.getCollideRect()
          clipRect2 = blobPos.clip(platPos)
          totalClipWidth += clipRect2.width
          if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
              if blobPos[0] < platPos[0] and blob._velocity.x >= 0:
                  if blob._velocity.x == 0:
                      blob._velocity.x = -100
                  else:
                      blob._velocity.x = -blob._velocity.x
              elif blobPos[0] + blobPos[2] > platPos[0] + platPos[2] and blob._velocity.x <= 0:
                  if blob._velocity.x == 0:
                      blob._velocity.x = 100
                  else:
                      blob._velocity.x = -blob._velocity.x
              if blob._velocity.y <= 0:
                  blob._velocity.y = -blob._velocity.y
              blob.manageState("fall")
          elif (clipRect2.width >= 5 or (clipRect2.width > 0 and totalClipWidth == 32)) and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
              blob.manageState("collidePlatform")
              i = False
          elif clipRect2.width < 5 and blob._FSM == "platformed" and i:
              blob.manageState("fall")
              blob.updateVisual()

      for category in level._traps:
          for trap in level._traps[category]:
              if blob.getCollideRect().colliderect(trap.getCollideRect()):
                  trap.handleCollision()
                  if category == "bra":
                      blob._velocity.x = -blob._velocity.x
                      blob.die()
                  elif category == "pan":
                      blob._velocity.x = -blob._velocity.x * 0.5
                      blob._velocity.y = -blob._velocity.y
                      blob.die()
                  elif category == "ring":
                      if blobPos[0] + blobPos[2] > trap.getCollideRect()[0] + trap.getCollideRect()[2]:
                          blob._velocity.x = 100
                      else:
                          blob._velocity.x = -100
                      blob._velocity.y = -blob._velocity.y

      for category4 in level._traps:
          for trap4 in level._traps[category4]:
              for zap4 in blob._zaps:
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
              for zap17 in blob._zaps:
                  if zap17.getCollideRect().colliderect(enemy17.getCollideRect()):
                      enemy17.handleCollision()
                      print(enemy17._hp)
                      zap17.handleDestroy()
                      if enemy17.isDead():
                          level._enemies[category17].remove(enemy17)

      for category21 in level._enemies:
          for enemy21 in level._enemies[category21]:
              if blob.getCollideRect().colliderect(enemy21.getCollideRect()):
                  blob._velocity.x = -blob._velocity.x
                  if category21 == "devil":
                      blob.die()

      for ring7 in level._traps["ring"]:
          for ringZap in ring7._zaps:
              for blobZap in blob._zaps:
                  if ringZap.getCollideRect().colliderect(blobZap.getCollideRect()):
                      ringZap.handleDestroy()
                      blobZap.handleDestroy()

      for gaston50 in level._enemies["gaston"]:
          for arrow50 in gaston50._arrows:
              for blobZap50 in blob._zaps:
                  if arrow50.getCollideRect().colliderect(blobZap50.getCollideRect()):
                      arrow50.handleDestroy()
                      blobZap50.handleDestroy()

      if blob._forcefield.isActive():
          for ring40 in level._traps["ring"]:
              for ringZap40 in ring40._zaps:
                  if ringZap40.getCollideRect().colliderect(blob._forcefield.getCollideRect()):
                      ringZap40.handleDestroy()

          for gaston82 in level._enemies["gaston"]:
              for arrow82 in gaston82._arrows:
                  if arrow82.getCollideRect().colliderect(blob._forcefield.getCollideRect()):
                      arrow82.handleDestroy()

      for ring20 in level._traps["ring"]:
          for zap20 in ring20._zaps:
              if zap20.getCollideRect().colliderect(blob.getCollideRect()):
                  zap20.handleDestroy()
                  blob.die()

      for gaston64 in level._enemies["gaston"]:
          for arrow64 in gaston64._arrows:
              if arrow64.getCollideRect().colliderect(blob.getCollideRect()):
                  arrow64.handleDestroy()
                  blob.die()

      for platform3 in level._platforms:
          for zap5 in blob._zaps:
              if zap5.getCollideRect().colliderect(platform3.getCollideRect()):
                  zap5.handleEnd()
          for ring15 in level._traps["ring"]:
              for zap15 in ring15._zaps:
                  if zap15.getCollideRect().colliderect(platform3.getCollideRect()):
                      zap5.handleEnd()
                  #blob._zaps.remove(zap5)


      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # handle arrow key up and down events
         else:
             blob.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000
      blob.update(WORLD_SIZE, ticks)
      for pan in level._traps["pan"]:
          pan.update(ticks)
      for zap2 in blob._zaps:
          zap2.update(WORLD_SIZE, ticks)
      for devil in level._enemies["devil"]:
          devil.update(WORLD_SIZE, ticks)
      for gaston in level._enemies["gaston"]:
          gaston.update(WORLD_SIZE, ticks)
      for ring in level._traps["ring"]:
          ring.update(WORLD_SIZE, ticks)

      if blob.isDead():
          print(deathCycle)
          if deathCycle > 30:
              level.reset()
              level.loadLevel()
              # initialize the blob on top of the ground
              blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))
              deathCycle = 0
          deathCycle += 1

      # getting the offset of the of the star (our tracking object)
      Drawable.updateOffset(blob, SCREEN_SIZE, WORLD_SIZE)

if __name__ == "__main__":
   main()
