import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os
from modules.frameManager import FRAMES

SPRITE_SIZE = Vector2(400, 75)

class Ceiling(Mobile):

    def __init__(self, position, final=False):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        super().__init__("ceiling.png", position, (0,0))
        self._hp = {"left": 0, "right": 0}
        self._final = final
        self._hitby = {"pink": False, "blue": False, "green": False, "orange": False}
        self._velocity = Vector2(0,0)

    def incHP(self, side, color="pink"):
        self._hp[side] += 1
        self._hitby[color] = True

    def allHit(self):
        for color in self._hitby:
            if self._hitby[color] == False:
                return False
        return True

    def readyForNextLevel(self):
        if self._final == False and self._hp["left"] + self._hp["right"] >= 6:
            return True
        elif self._final == True and self.allHit() and self._hp["left"] + self._hp["right"] > 17:
            return True
        return False


    def updateVisual(self):
        if (self._hp["left"] > 2 or self._hp["right"] > 2):
            if self._hp["left"] > 2 and self._hp["right"] < 2:
                self._imageName = "ceiling3.png"
            elif self._hp["right"] > 2  and self._hp["left"] < 2:
                self._imageName = "ceiling4.png"
            elif self._hp["left"] + self._hp["right"] < 8:
                self._imageName = "ceiling5.png"
            elif self._hp["left"] + self._hp["right"] < 12 and self._final:
                self._imageName = "ceiling6.png"
            elif self._hp["left"] + self._hp["right"] <= 16 and self._final:
                self._imageName = "ceiling7.png"
            elif self._hp["left"] + self._hp["right"] > 17 and self._final:
                self._imageName = "broken.png"
                self._velocity = Vector2(0,100)
        else:
            self._imageName = "ceiling.png"
        self._image = FRAMES.getFrame(self._imageName, (0,0))

    def update(self, ticks):
        super().update(ticks)
