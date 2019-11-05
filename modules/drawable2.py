"""
Abby Nason
Project 2
drawable.py

Defines the Drawable class.
"""

import pygame
import os
from modules.vector2D import Vector2

class Drawable:
    WINDOW_OFFSET = [0,0]

    def __init__(self, imageName, position, rect=None, transparent=True):
        """initializes to orb class with instance variables: _imageName,
        _image, and _position"""
        self._imageName = imageName
        # load the image given in the parameters
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        # if there is a rect parameter, create the collide rect
        if rect != None:
            self._image = pygame.Surface((rect.width,rect.height))
            self._image.blit(fullImage, (0,0), rect)
        # otherwise use the image's dimensions for the surface
        else:
            self._image = pygame.Surface((fullImage.get_rect().width, fullImage.get_rect().height))
            self._image.blit(fullImage, (0,0))
        #if transparent get the color key
        if transparent == True:
            self._image.set_colorkey(self._image.get_at((0,0)))
        #a vector2 of its position in the world
        self._position = position

    def getWidth(self):
        """returns the width of the image surface"""
        return self._image.get_width()

    def getHeight(self):
        """returns the heighto of the image surface"""
        return self._image.get_height()

    def getPosition(self):
        """returns the current position"""
        return self._position

    def setPosition(self, newPosition):
        self._position = newPosition

    def getX(self):
        """returns the x coordinate of the current position"""
        return self._position.x

    def getY(self):
        """returns the y coordinate of the current position"""
        return self._position.y

    def getSize(self):
        """returns the size of the image surface"""
        return self._image.get_size()

    def getCollideRect(self):
        return self._position + pygame.Rect(self._image.get_rect())

    def draw(self, surface):
        """draws the image at the current position on the surface"""
        #blits the pygame surface of orb.png to the surface passed in the parameters based on the offset
        surface.blit(self._image, (self._position.x - Drawable.WINDOW_OFFSET[0], self._position.y - Drawable.WINDOW_OFFSET[1]))

    @classmethod
    def updateOffset(cls, trackingObject, screenSize, worldSize):
        """updates the WINDOW_OFFSET class variable"""
        offset = Vector2(min(max(0,
                                 trackingObject.getX() + (trackingObject.getWidth() // 2) - (screenSize[0] // 2)),
                             worldSize[0] - screenSize[0]),
                         min(max(0,
                                 trackingObject.getY() + (trackingObject.getHeight() // 2) - (screenSize[1] // 2)),
                         worldSize[1] - screenSize[1]))
        # update the WINDOW_OFFSET class variable
        Drawable.WINDOW_OFFSET = offset

    @classmethod
    def adjustMousePos(cls, mousePos):
        """adjusts the mouse position on screen to coordinates within the wider world"""
        adjustedPos = [mousePos[0] + Drawable.WINDOW_OFFSET[0], mousePos[1] + Drawable.WINDOW_OFFSET[1]]
        return Vector2(adjustedPos[0], adjustedPos[1])
