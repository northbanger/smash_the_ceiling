"""
Abby Nason
smash! the ceiling
devil.py

Create the tasmanian devil enemy.
"""
import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
from characters.blobzap import BlobZap
import os

SPRITE_SIZE = Vector2(32, 32)
MAX_VELOCITY = 50
ACCELERATION = 5.0

class Devil(Mobile):

    def __init__(self, position, patrolUnit):
        """initializes a devil object"""
        super().__init__("dizzy_devil.png", position, (0,1))
        #a vector2 of its velocity
        self._velocity = Vector2(MAX_VELOCITY,0)
        self._startPosition = position
        self._maxVelocity = MAX_VELOCITY
        self._acceleration = ACCELERATION
        self._patrolLength = patrolUnit * 50 - SPRITE_SIZE.x
        self._vSpeed = 100
        self._waitTime = 0.75
        self._waitTimer = 0
        self._right = True
        self._patrolRect = pygame.Rect(self._position.x, self._position.y, self._patrolLength, SPRITE_SIZE.y)
        self._hp = 25

    def handleCollision(self):
       """decreases hit points when collided with"""
       self._hp -= 1

    def isDead(self):
        """returns true if hitpoints less than 0"""
        return self._hp <= 0
    # Public access to tell jumper to try to take some action, typically for collision
    def manageState(self, action):
      self._FSM.manageState(action)

    def update(self, worldInfo, ticks):
      """updates the movement of the devil based on the defined patrolling parameters"""
      newPosition = self._position
      if not self._patrolRect.collidepoint(self._position.x, self._position.y):
          if self._right and self._waitTimer == 0:
              self._right = False
          elif self._waitTimer == 0:
              self._right = True
          self._velocity.x = 0
          self._waitTimer += ticks
          if self._waitTimer > self._waitTime:
              if self._right:
                  self._velocity.x = MAX_VELOCITY
              else:
                  self._velocity.x = -MAX_VELOCITY
              self._waitTimer = 0
      self._position.x += self._velocity.x * ticks
      self.updateVisual()

    def updateVisual(self):
        """update the animation of the devil based on its current movement"""
        #facing right stopped
        if self._waitTimer > 0 and self._right:
            fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
            #rect = pygame.Rect(SPRITE_SIZE.y * 8, SPRITE_SIZE.y * 4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            rect = pygame.Rect(SPRITE_SIZE.y * 7 + 20, SPRITE_SIZE.y * 4 + 4, SPRITE_SIZE.x - 3, SPRITE_SIZE.y)
            self._image = pygame.Surface((rect.width,rect.height))
            self._image.blit(fullImage, (0,0), rect)
            self._image.set_colorkey(self._image.get_at((0,0)))
        #facing left stopped
        elif self._waitTimer > 0 and not self._right:
            fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
            #rect = pygame.Rect(SPRITE_SIZE.y * 7, SPRITE_SIZE.y * 4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            rect = pygame.Rect(SPRITE_SIZE.y * 6 + 2, SPRITE_SIZE.y * 4 + 4, SPRITE_SIZE.x - 6, SPRITE_SIZE.y)
            self._image = pygame.Surface((rect.width,rect.height))
            self._image.blit(fullImage, (0,0), rect)
            self._image.set_colorkey(self._image.get_at((0,0)))
        #moving left
        elif self._waitTimer == 0 and not self._right:
            fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
            #rect = pygame.Rect(SPRITE_SIZE.y * 2, SPRITE_SIZE.y * 4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            rect = pygame.Rect(SPRITE_SIZE.y * 1 + -3, SPRITE_SIZE.y * 4 +4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            self._image = pygame.Surface((rect.width,rect.height))
            self._image.blit(fullImage, (0,0), rect)
            self._image.set_colorkey(self._image.get_at((0,0)))
        #moving right
        elif self._waitTimer == 0 and self._right:
            fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
            #rect = pygame.Rect(SPRITE_SIZE.y * 2, SPRITE_SIZE.y * 4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            rect = pygame.Rect(SPRITE_SIZE.y * 0 + 2, SPRITE_SIZE.y * 4 +4, SPRITE_SIZE.x, SPRITE_SIZE.y)
            self._image = pygame.Surface((rect.width,rect.height))
            self._image.blit(fullImage, (0,0), rect)
            self._image.set_colorkey(self._image.get_at((0,0)))
