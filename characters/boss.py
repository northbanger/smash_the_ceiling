"""
Abby Nason
smash! the ceiling
blobzap.py

Creates a boss enemy that pits other women against the blob.
"""
import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.animated import Animated
from modules.frameManager import FrameManager
from characters.spawn import Spawn
from characters.ringzap import RingZap

SPRITE_SIZE = Vector2(30,40)

class Boss(Animated):
    def __init__(self, position):
        """intializes a boss enemy"""
        position.y -= 6
        super().__init__("boss.png", position, (0,0))
        self._originalPosition = position
        self._row = 0
        self._nFrames = 2
        self._spawns = []
        self._spawnTimer = 0
        self._spawnTime = 3
        self._framesPerSecond = 5.0
        self._hp = 150

    def handleCollision(self):
        """decreases hit points when collision happens"""
        self._hp -= 1

    def isDead(self):
        """determines if enemy is dead"""
        return self._hp <= 0

    def getCollideRect(self):
       """decreases collide rect size"""
       newRect =  self._position + self._image.get_rect()
       newRect = pygame.Rect(self._position.x + 5, self._position.y + 25, SPRITE_SIZE.x - 1, SPRITE_SIZE.y)
       return newRect

    def update(self, worldInfo, ticks):
        """updates the boss animation and the positions of its spawns"""
        super().update(ticks, True)
        for blob in self._spawns:
            blob.update(worldInfo, ticks)
        self._spawnTimer += ticks
        if self._spawnTimer > self._spawnTime:
            spawn = Spawn(Vector2(self._position.x,self._position.y+32+25-9), SPRITE_SIZE)
            self._spawns.append(spawn)
            self._spawnTimer = 0
        #self._position = self._originalPosition
