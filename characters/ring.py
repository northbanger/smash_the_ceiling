import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable

SPRITE_SIZE = Vector2(32, 32)


class Ring(Drawable):
    def __init__(self, position):
       super().__init__("weddingring.png", position, (0,0))
       self._ranInto = False

    def ranInto(self):
        return self._ranInto

    def handleCollision(self):
        self._ranInto = True
        #self._imageName = "explosion.png"
        #fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        #rect = pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)
        #self._image = pygame.Surface((rect.width,rect.height))
        #self._image.blit(fullImage, (0,0), rect)
        #self._image.set_colorkey(self._image.get_at((0,0)))
