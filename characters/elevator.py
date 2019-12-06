"""
Abby Nason
smash! the ceiling
elevator.py

Create the elevator to transition between levels.
"""
import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable

MAIN_SPRITE_SIZE = Vector2(50, 20)
LITTLE_SPRITE_SIZE = Vector2(50,10)


class Elevator:
    def __init__(self, position, worldHeight):
       """initializes an elevator object"""
       self._position = position
       self._parts = {"back": [], "front": [], "doors": [], "top": []}
       totalHeight = worldHeight-(50 + MAIN_SPRITE_SIZE.x)
       for i in range(0, totalHeight, MAIN_SPRITE_SIZE.y):
           self._parts["back"].append(Drawable("elevator_back.png", Vector2(self._position.x,i), (0,0)))
       for j in range(0, totalHeight-60, MAIN_SPRITE_SIZE.y):
           self._parts["front"].append(Drawable("elevator_front.png", Vector2(self._position.x,j), (0,0)))
       for k in range(totalHeight-60, totalHeight, MAIN_SPRITE_SIZE.y):
           self._parts["doors"].append(Drawable("elevator_doors.png", Vector2(self._position.x,k), (0,0)))
       self._parts["top"].append(Drawable("elevator_top.png", Vector2(self._position.x, totalHeight-60), (0,0)))
       self._ranInto = False

    def ranInto(self):
        """returns true if blob ran into elevator"""
        return self._ranInto

    def getCollideRect(self):
       """returns a smaller collide rect to make sure the blob is fully inside
       the elevator drawing"""
       newRect =  self._position + self._image.get_rect()
       newRect = pygame.Rect(self._position.x + 10, self._position.y - 2, SPRITE_SIZE.x - 20, SPRITE_SIZE.y - 2)
       return newRect

    def handleCollision(self):
        """set ranInto to true if it has been collided with"""
        self._ranInto = True
