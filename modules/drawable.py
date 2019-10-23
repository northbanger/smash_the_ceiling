import pygame
from pygame import image
import os
from .frameManager import FRAMES
from modules.vector2D import Vector2

class Drawable(object):
   WINDOW_OFFSET = [0,0]

   def __init__(self, imageName, position, offset=None):
      self._imageName = imageName

      # Let frame manager handle loading the image
      self._image = FRAMES.getFrame(self._imageName, offset)

      self._position = position

   def getPosition(self):
      return self._position

   def setPosition(self, newPosition):
      self._position = newPosition

   def getSize(self):
      return self._image.get_size()

   def getCollideRect(self):
      newRect =  self._position + self._image.get_rect()
      return newRect

   def getX(self):
       """returns the x coordinate of the current position"""
       return self._position.x

   def getY(self):
       """returns the y coordinate of the current position"""
       return self._position.y

   def getWidth(self):
       """returns the width of the image surface"""
       return self._image.get_width()

   def getHeight(self):
       """returns the heighto of the image surface"""
       return self._image.get_height()

   def draw(self, surface):
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
