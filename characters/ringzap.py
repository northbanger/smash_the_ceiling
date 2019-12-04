"""
Abby Nason
smash! the ceiling
ringzap.py

Creates the ringzaps.
"""

import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os
import random

SPRITE_SIZE = Vector2(16, 16)
MAX_VELOCITY = 150
ACCELERATION = 5.0
ZAP_RANGE = 50

class RingZap(Mobile):

    def __init__(self, position, spriteSize):
        """initializes a ring zap object"""
        direction = random.randint(1,10)
        self._movement = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False}
        #randomly determines direction of movement
        if direction < 5:
            self._movement[pygame.K_LEFT] = True
            position = Vector2(position.x - spriteSize.x, position.y + spriteSize.y//2 - 16)
        elif direction < 8:
            self._movement[pygame.K_RIGHT] = True
            position = Vector2(position.x + spriteSize.x, position.y + spriteSize.y//2 - 16)
        else:
            self._movement[pygame.K_UP] = True
            position = Vector2(position.x + 6, position.y - 6)
        super().__init__("bubble_enemies.png", position, (2,10))
        #a vector2 of its velocity
        self._originalPosition = position
        self._velocity = Vector2(MAX_VELOCITY,MAX_VELOCITY)
        self._active = True
        self._notActiveCount = 0
        self._zapTimer = 0
        self._zapTime = 0.75
        self._start = True

    def isActive(self):
        """returns if the zap is active or not"""
        return self._active

    def incNotActive(self):
        """increment the count of it not being active"""
        self._notActiveCount += 1

    def notActive(self):
        """returns the amount it has not been active"""
        return self._notActiveCount

    def handleEnd(self):
        """handle the animation of the zap timing out"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 5, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

    def handleDestroy(self):
        """handle the animation of a violent collision"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 4, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

    def update(self, worldInfo, ticks):
      """update the position of the zap based on the direction it was
      shot off in"""
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._active = False
      self._zapTimer += ticks
      if self._zapTimer > self._zapTime:
          #self._active = False
          self.handleEnd()
      if self._movement[pygame.K_LEFT]:
          self._position.x += -self._velocity.x * ticks
      elif self._movement[pygame.K_UP]:
          self._position.y += -self._velocity.y * ticks
      else:
          self._position.x += self._velocity.x * ticks
