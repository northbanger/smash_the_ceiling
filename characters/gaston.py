"""
Abby Nason
smash! the ceiling
gaston.py

Create the gaston enemy.
"""
import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.animated import Animated
from modules.frameManager import FrameManager
from characters.arrow import Arrow
from characters.ringzap import RingZap

SPRITE_SIZE = Vector2(30,40)

class Gaston(Animated):
    def __init__(self, position):
        """intializes a gaston object"""
        position.y -= 6
        super().__init__("gaston.png", position, (1,1))
        self._originalPosition = position
        self._row = 1
        self._nFrames = 5
        self._arrows = []
        self._arrowTimer = 0
        self._arrowTime = 1
        self._framesPerSecond = 5.0
        self._hp = 50

    def handleCollision(self):
       """decreases hit points if collided with"""
       self._hp -= 1

    def isDead(self):
        """kills gaston"""
        return self._hp <= 0

    def update(self, worldInfo, ticks):
        """updates gaston's animation and the movement of the arrows"""
        super().update(ticks, True)
        for arrow in self._arrows:
            arrow.update(worldInfo, ticks)
        self._arrowTimer += ticks
        if self._arrowTimer > self._arrowTime:
            arrow = Arrow(self._position, SPRITE_SIZE)
            self._arrows.append(arrow)
            self._arrowTimer = 0
        #self._position = self._originalPosition
