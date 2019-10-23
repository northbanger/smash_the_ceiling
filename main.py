"""
Abby Nason
Project 1
main.py

Displays a star which moves based on arrow key input. When the mouse is clicked, an orb is
introduced to the world at that position and moves in a random direction. When the star and
an orb collide, the orb "dies" and is removed from the game. Both star and orb objects rebound
against the edge of the world The window follows the star around the world.
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
   platform1a = Drawable("platform.png", Vector2(150, 200), (0,0))
   platform1b = Drawable("platform.png", Vector2(200, 200), (0,0))
   platform2a = Drawable("platform.png", Vector2(400, 250), (0,0))
   platform3a = Drawable("platform.png", Vector2(475, 150), (0,0))
   platform3b = Drawable("platform.png", Vector2(525, 150), (0,0))
   platform3c = Drawable("platform.png", Vector2(575, 150), (0,0))
   platform4a = Drawable("platform.png", Vector2(600, 150), (0,0))
   platform4b = Drawable("platform.png", Vector2(650, 150), (0,0))
   platform4c = Drawable("platform.png", Vector2(700, 150), (0,0))
   platform5a = Drawable("platform.png", Vector2(625, 275), (0,0))
   platform5b = Drawable("platform.png", Vector2(675, 275), (0,0))
   platform6a = Drawable("platform.png", Vector2(750, 250), (0,0))
   platform7a = Drawable("platform.png", Vector2(1000, 200), (0,0))
   platform7b = Drawable("platform.png", Vector2(1050, 200), (0,0))
   platform8a = Drawable("platform.png", Vector2(1125, 100), (0,0))
   platform8b = Drawable("platform.png", Vector2(1175, 100), (0,0))
   platform9a = Drawable("platform.png", Vector2(1500, 200), (0,0))
   platform9b = Drawable("platform.png", Vector2(1550, 200), (0,0))
   platform9c = Drawable("platform.png", Vector2(1600, 200), (0,0))
   platforms = [platform1a, platform1b, platform2a, platform3a, platform3b, platform3c, platform4a, platform4b, platform4c, platform5a, platform5b, platform6a, platform7a, platform7b, platform8a, platform8b, platform9a, platform9b, platform9c]

   bra = Bra(Vector2(200,300-CHAR_SPRITE_SIZE.y))
   traps.append(bra)
   pan = Pan(Vector2(400,300-CHAR_SPRITE_SIZE.y))
   traps.append(pan)
   ring = Ring(Vector2(200,200-CHAR_SPRITE_SIZE.y))
   traps.append(ring)

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

   # main loop
   while RUNNING:

      gameClock.tick()

      # draw everything based on the offset
      #screen.blit(background, (-offset[0], -offset[1]))
      background.draw(screen)
      ground.draw(screen)
      for platform2 in platforms:
          platform2.draw(screen)
      for trap2 in traps:
          trap2.draw(screen)
      blob.draw(screen)
      #for orb in orbs:
        #orb.draw(screen)

      for trap3 in traps:
          if trap3.ranInto():
              if trap3 == bra:
                  traps.remove(trap3)
              elif trap3 == pan:
                  trap.resetRanInto()
      # flip display to the monitor
      pygame.display.flip()

      clipRect = blob.getCollideRect().clip(ground.getCollideRect())

      if clipRect.width > 0:
         blob.manageState("collideGround")

      #variable to determine if already collided with a platform
      i = True
      blobPos = blob.getCollideRect()
      for platform in platforms:
          platPos = platform.getCollideRect()
          print(platPos)
          clipRect2 = blobPos.clip(platPos)
          print(clipRect2.width > 0)
          print(blob._FSM._state)
          print(blobPos[1] - 90)
          print(platPos[1] + platPos[3])
          print()
          #if clipRect2.width > 0 and blob._FSM == "jumping" and blobPos[1] - 10 <= platPos[1] + platPos[3]:
        #      blob.manageState("fall")
          if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
              blob._velocity.x = -blob._velocity.x
              blob._velocity.y = -blob._velocity.y
              blob.manageState("fall")
          elif clipRect2.width >= 5 and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
              blob.manageState("collidePlatform")
              i = False
          elif clipRect2.width < 5 and blob._FSM == "platformed" and i:
              print("FALL")
              blob.manageState("fall")
              blob.updateVisual()

      for trap in traps:
          if blob.getCollideRect().colliderect(trap.getCollideRect()):
              trap.handleCollision()
              if trap == bra:
                  blob._velocity.x = -blob._velocity.x
              elif trap == pan:
                  blob._velocity.x = -blob._velocity.x * 0.5
                  blob._velocity.y = -blob._velocity.y

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # only do something if mouse button is down
         elif event.type == pygame.MOUSEBUTTONDOWN:
             #add an orb to the adjusted location in the world
             adjustedPos = Drawable.adjustMousePos(list(event.pos))
             #orbs.append(Orb(adjustedPos))
         # handle arrow key up and down events
         else:
             blob.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000
      blob.update(WORLD_SIZE, ticks)
      pan.update(ticks)
      #for orb in orbs:
        #orb.update(WORLD_SIZE, ticks)

      # Detect collision
      #for orb in orbs:
        #  if orb.getCollideRect().colliderect(star.getCollideRect()):
        #      orb.kill()

      # remove the dead orbs before the next iteration
      #for orb in orbs:
        #  if orb.isDead():
        #      orbs.remove(orb)

      # getting the offset of the of the star (our tracking object)
      Drawable.updateOffset(blob, SCREEN_SIZE, WORLD_SIZE)

if __name__ == "__main__":
   main()
