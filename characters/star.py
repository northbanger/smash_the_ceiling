"""
Abby Nason
Project 2
star.py

Defines the Star class, which inherits from the Drawable class.
"""

import pygame
from vector2D import Vector2
from drawable import Drawable

SPRITE_SIZE = Vector2(32, 32)
MAX_VELOCITY = 75
ACCELERATION = 5.0

class Star(Drawable):

    def __init__(self, position):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        super().__init__("blobs.png", position, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y), True)
        #a vector2 of its velocity
        self._velocity = Vector2(0,0)
        self._maxVelocity = MAX_VELOCITY
        self._acceleration = ACCELERATION
        self._movement = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

    def move(self, event):
        """sets the values in the _movement dictionary based on which arrow keys
        are up (False) and which keys are down (True)"""
        #keydown event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self._movement[pygame.K_DOWN] = True
            elif event.key == pygame.K_UP:
                self._movement[pygame.K_UP] = True
            elif event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = True
            elif event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = True
        #keyup event
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self._movement[pygame.K_DOWN] = False
            elif event.key == pygame.K_UP:
                self._movement[pygame.K_UP] = False
            elif event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = False
            elif event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = False

    def update(self, worldInfo, ticks):
        """updates the star's position based on its current velocity"""
        #handle velocity according to the keys that are pressed
        if self._movement[pygame.K_DOWN]:
            self._velocity.y += self._acceleration
        if self._movement[pygame.K_UP]:
            self._velocity.y += -self._acceleration
        if self._movement[pygame.K_LEFT]:
            self._velocity.x += -self._acceleration
        if self._movement[pygame.K_RIGHT]:
            self._velocity.x += self._acceleration

        #scale the velocity if the star's magnitude exceeds max velocity
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        #handle if the star is going to exceed the world bounds
        newPosition = self._position + self._velocity * ticks
        if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
            self._velocity.x = -self._velocity.x
        if newPosition[1] < 0 or newPosition[1] > worldInfo[1]:
            self._velocity.y = -self._velocity.y
        newPosition = self._position + self._velocity * ticks
        self._position = newPosition
