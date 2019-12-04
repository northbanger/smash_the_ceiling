"""
Abby Nason
smash! the ceiling
powerup.py

Creates all of the powerups.
"""
import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable

SPRITE_SIZE = Vector2(32, 32)


class Floppy(Drawable):
    def __init__(self, position):
       """intializes a floppy object"""
       super().__init__("powerup.png", position, (0,0))
       self._active = True
       self._notActiveCount = 0

    def isActive(self):
        """determines if the powerup is active"""
        return self._active

    def incNotActive(self):
        """increments the count of the time it has been inactive"""
        self._notActiveCount += 1

    def notActive(self):
        """returns the count of inactivity"""
        return self._notActiveCount

    def handleEnd(self):
        """handles removing the powerup from the screen gracefully"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 5, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

class Sign(Drawable):
    """intializes a sign object"""
    def __init__(self, position):
       super().__init__("powerup2.png", position, (0,0))
       self._active = True
       self._notActiveCount = 0

    def isActive(self):
        """determines if the powerup is active"""
        return self._active

    def incNotActive(self):
        """increments the count of the time it has been inactive"""
        self._notActiveCount += 1

    def notActive(self):
        """returns the count of inactivity"""
        return self._notActiveCount

    def handleEnd(self):
        """handles removing the powerup from the screen gracefully"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 5, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

class Vote(Drawable):
    """intializes a vote object"""
    def __init__(self, position):
       super().__init__("powerup3.png", position, (0,0))
       self._active = True
       self._notActiveCount = 0

    def isActive(self):
        """determines if the powerup is active"""
        return self._active

    def incNotActive(self):
        """increments the count of the time it has been inactive"""
        self._notActiveCount += 1

    def notActive(self):
        """returns the count of inactivity"""
        return self._notActiveCount

    def handleEnd(self):
        """handles removing the powerup from the screen gracefully"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 5, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False
