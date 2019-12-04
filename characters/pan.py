"""
Abby Nason
smash! the ceiling
pan.py

Create the frying pan trap.
"""
import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.animated import Animated
from modules.frameManager import FrameManager

SPRITE_SIZE = Vector2(32, 32)


class Pan(Animated):
    def __init__(self, position):
        """intializes a pan object"""
        super().__init__("fryingpan.png", position, (0,0))
        self._row = 0
        self._nFrames = 4
        self._ranInto = False

    def ranInto(self):
        """determines if the trap has been run into"""
        return self._ranInto

    def getCollideRect(self):
       """make the height of the collide rect shorter"""
       newRect =  self._position + self._image.get_rect()
       newRect = Vector2(0, 16) + newRect
       return newRect

    def resetRanInto(self):
        """reset if it has been run into"""
        self._ranInto = False

    def handleCollision(self):
        """assigns boolean to true if trap has been run into"""
        self._ranInto = True
