import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
import os
from modules.frameManager import FRAMES

SPRITE_SIZE = Vector2(400, 75)

class Ceiling(Drawable):

    def __init__(self, position, final=False):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        super().__init__("ceiling.png", position, (0,0))
        self._hp = {"left": 0, "right": 0}
        self._final = final

    def incHP(self, side):
        self._hp[side] += 1

    def readyForNextLevel(self):
        if self._final == False and self._hp["left"] + self._hp["right"] >= 6:
            return True
        return False


    def updateVisual(self):
        if (self._hp["left"] > 2 or self._hp["right"] > 2):
            if self._hp["left"] > 2 and self._hp["right"] < 2:
                self._imageName = "ceiling3.png"
            elif self._hp["right"] > 2  and self._hp["left"] < 2:
                self._imageName = "ceiling4.png"
            elif self._hp["left"] + self._hp["right"] > 4:
                self._imageName = "ceiling5.png"
        else:
            self._imageName = "ceiling.png"
        self._image = FRAMES.getFrame(self._imageName, (0,0))
