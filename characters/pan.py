import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.animated import Animated
from modules.frameManager import FrameManager

SPRITE_SIZE = Vector2(32, 32)


class Pan(Animated):
    def __init__(self, position):
        super().__init__("fryingpan.png", position, (0,0))
        self._row = 0
        self._nFrames = 4
        self._ranInto = False

    def ranInto(self):
        return self._ranInto

    def getCollideRect(self):
       newRect =  self._position + self._image.get_rect()
       newRect = Vector2(0, 16) + newRect
       return newRect

    def resetRanInto(self):
        self._ranInto = False

    def handleCollision(self):
        self._ranInto = True
        #self._imageName = "explosion.png"
        #fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        #rect = pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)
        #self._image = pygame.Surface((rect.width,rect.height))
        #self._image.blit(fullImage, (0,0), rect)
        #self._image.set_colorkey(self._image.get_at((0,0)))
