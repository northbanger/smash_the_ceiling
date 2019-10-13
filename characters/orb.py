"""
Abby Nason
Project 2
orb.py

Defines the Orb class, which inherits from the Drawable class.
"""

import pygame
from modules.drawable import Drawable
from modules.vector2D import Vector2
import random

SPRITE_SIZE = Vector2(32,32)
STANDARD_SPEED = 50

class Orb(Drawable):

    def __init__(self, position):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity and _dead"""
        super().__init__("orbs.png", position, pygame.Rect(SPRITE_SIZE.x * random.randint(0, 10), 0, SPRITE_SIZE.x, SPRITE_SIZE.y), True)
        #a vector2 of its velocity
        self._velocity = Vector2(random.randint(-100, 100), random.randint(-100,100))
        #scale the vector so its the correct speed upon intialization
        self._velocity.scale(STANDARD_SPEED)
        #keeps track the the orb has collided with a star or not
        self._dead = False

    def update(self, worldInfo, ticks):
        """updates the orb's position based on its current velocity"""
        # calculates new position
        newPosition = self._position + self._velocity * ticks
        #handles if the the orb will go outside world coordinates
        if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
            self._velocity.x = -self._velocity.x
        if newPosition[1] < 0 or newPosition[1] > worldInfo[1]:
            self._velocity.y = -self._velocity.y
        # recalculates the new psoition
        newPosition = self._position + self._velocity * ticks
        # resets the instance variable
        self._position = newPosition

    def kill(self):
        """sets _dead instance variable to True"""
        self._dead = True

    def isDead(self):
        """returns the _dead instance variable"""
        return self._dead
