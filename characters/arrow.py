"""
Abby Nason
smash! the ceiling
main.py

Creates gaston's arrow.
"""
import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os
import random

SPRITE_SIZE = Vector2(24, 40)
MAX_VELOCITY = 150
ACCELERATION = 5.0
ZAP_RANGE = 50

class Arrow(Mobile):

    def __init__(self, position, spriteSize):
        """intializes an arrow object"""
        #adjust position correctly before creating it
        position = Vector2(position.x - spriteSize.x//2, position.y)
        super().__init__("gaston.png", position, (0,1))
        self._originalPosition = position
        self._velocity = Vector2(MAX_VELOCITY,MAX_VELOCITY)
        self._active = True
        self._notActiveCount = 0
        self._zapTimer = 0
        self._zapTime = 0.8
        self._start = True

    def isActive(self):
        """returns arrow is active"""
        return self._active

    def incNotActive(self):
        """increments count of not being active for purposes of end aniamtion"""
        self._notActiveCount += 1

    def notActive(self):
        """sets arrow as not active"""
        return self._notActiveCount

    def handleEnd(self):
        """handle an arrow timing out of activity"""
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
        """handle an arrow colliding violently"""
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
      """update the position of the arrow"""
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._active = False
      self._zapTimer += ticks
      if self._zapTimer > self._zapTime:
          #self._active = False
          self.handleEnd()
      self._position.x += -self._velocity.x * ticks
      #super().update(ticks)
