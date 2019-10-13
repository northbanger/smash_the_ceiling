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

   # instantiating the background as a Drawable object
   background = Drawable("background.png", Vector2(0,0), transparent=False)
   ground = Drawable("ground2.png", Vector2(0, 300), transparent=False)

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
      blob.draw(screen)
      #for orb in orbs:
        #orb.draw(screen)

      # flip display to the monitor
      pygame.display.flip()

      clipRect = blob.getCollideRect().clip(ground.getCollideRect())

      if clipRect.width > 0:
         blob.manageState("collideGround")

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
      blob.update(ticks)
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
