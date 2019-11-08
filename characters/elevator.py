import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable

MAIN_SPRITE_SIZE = Vector2(50, 20)
LITTLE_SPRITE_SIZE = Vector2(50,10)


class Elevator(Drawable):
    def __init__(self, position, worldHeight):
       self._position = position
       self._parts = {"back": [], "front": [], "doors": [], "top": []}
       totalHeight = worldHeight-(100 + MAIN_SPRITE_SIZE.x)
       for i in range(0, totalHeight, MAIN_SPRITE_SIZE.y):
           self._parts["back"].append(Drawable("elevator_back.png", Vector2(self._position.x,i), (0,0)))
       for j in range(0, totalHeight-60, MAIN_SPRITE_SIZE.y)
           self._parts["front"].append(Drawable("elevator_front.png", Vector2(self._position.x,j), (0,0)))
       for k in range(3):
           self._parts.append(Drawable("elevator_doors.png", Vector2(self._position.x,k), (0,0)))
       self._parts.append(Drawable("elevator_top.png", ))
       self._ranInto = False

    def ranInto(self):
        return self._ranInto

    def getCollideRect(self):
       newRect =  self._position + self._image.get_rect()
       newRect = pygame.Rect(self._position.x + 10, self._position.y - 2, SPRITE_SIZE.x - 20, SPRITE_SIZE.y - 2)
       return newRect

    def handleCollision(self):
        self._ranInto = True
        #self._imageName = "explosion.png"
        #fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        #rect = pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)
        #self._image = pygame.Surface((rect.width,rect.height))
        #self._image.blit(fullImage, (0,0), rect)
        #self._image.set_colorkey(self._image.get_at((0,0)))
