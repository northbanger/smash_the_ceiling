"""
Abby Nason
smash! the ceiling
ring.py

Creates the ring trap.
"""

import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from characters.ringzap import RingZap

SPRITE_SIZE = Vector2(32, 32)


class Ring(Drawable):
    def __init__(self, position):
       """intializes a ring object"""
       super().__init__("weddingring.png", position, (0,0))
       self._ranInto = False
       self._zaps = []
       self._zapTime = 0.75
       self._zapTimer = 0

    def ranInto(self):
        """determines if ring has been ran into"""
        return self._ranInto

    def getCollideRect(self):
        """decrease the collide rect"""
        newRect =  self._position + self._image.get_rect()
        newRect = pygame.Rect(self._position.x + 10, self._position.y - 2, SPRITE_SIZE.x - 20, SPRITE_SIZE.y - 2)
        return newRect

    def update(self, worldInfo, ticks):
        """update the movement and spawning of the zaps"""
        for zap in self._zaps:
            zap.update(worldInfo, ticks)
        self._zapTimer += ticks
        if self._zapTimer > self._zapTime:
            zap = RingZap(self._position, SPRITE_SIZE)
            self._zaps.append(zap)
            self._zapTimer = 0

    def handleCollision(self):
        """set the boolean determining if the ring has been ran into to true"""
        self._ranInto = True
