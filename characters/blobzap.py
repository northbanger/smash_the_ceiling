import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os

SPRITE_SIZE = Vector2(16, 16)
MAX_VELOCITY = 250
ACCELERATION = 5.0
ZAP_RANGE = 50

class BlobZap(Mobile):

    def __init__(self, position):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        #super().__init__("blobs.png", position, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)) #, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y), True)
        super().__init__("nuts_and_milk.png", position, (11,1))
        #a vector2 of its velocity
        self._originalPosition = position
        self._velocity = Vector2(MAX_VELOCITY,0)
        #self._maxVelocity = MAX_VELOCITY
        #self._acceleration = ACCELERATION
        self._active = True
        self._zapTimer = 0
        self._zapTime = 0.75
        self._movement = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        self._start = True

    def isActive(self):
        return self._active

    def handleEvent(self, event):
      # attempt to manage state based on keypresses
      if self._start:
          self._start = False
          if event:
            self._movement[pygame.K_LEFT] = True
            self._movement[pygame.K_RIGHT] = False
          else:
            self._movement[pygame.K_LEFT] = False
            self._movement[pygame.K_RIGHT] = True

    def update(self, worldInfo, ticks):
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._active = False
      self._zapTimer += ticks
      if self._zapTimer > self._zapTime:
          self._active = False
      #print(self._movement[pygame.K_LEFT])
      if self._movement[pygame.K_LEFT]:
          self._position.x += -self._velocity.x * ticks
      else:
          self._position.x += self._velocity.x * ticks
      #super().update(ticks)
