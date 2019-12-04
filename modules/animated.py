"""
Professor Matthews
smash! the ceiling
animated.py

Creates an animation object.
"""

import pygame
from pygame import image
import os
from .frameManager import FRAMES
from .drawable import Drawable

class Animated(Drawable):

   def __init__(self, imageName, location, offset=None):
      super().__init__(imageName, location, offset)

      self._frame = 0
      self._row = 0
      self._animationTimer = 0
      self._framesPerSecond = 10.0
      self._nFrames = 2

      self._animate = True

   def update(self, ticks, gaston=False):
      if self._animate:
         self._animationTimer += ticks

         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            if self._frame == 0 and gaston:
                self._frame = 1
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))

   def startAnimation(self):
      self._animate = True

   def stopAnimation(self):
      self._animate = False
