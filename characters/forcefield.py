import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile

SPRITE_SIZE = Vector2(32, 32)
MAX_VELOCITY = 150
ACCELERATION = 5.0



class Forcefield(Mobile):
    def __init__(self, position, velocity):
       super().__init__("forcefield.png", position, (0,0))
       self._powerUpTime = 5
       self._powerUpTimer = 0
       self._active = False
       self._velocity = velocity
       self._maxVelocity = MAX_VELOCITY
       self._acceleration = ACCELERATION
       self._movement = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
       self._jumpTimer = 0
       self._jumpTime = 0.75
       self._vSpeed = 100
       self._jSpeed = 80

    def isActive(self):
        return self._active

    def manageState(self, action):
        self._FSM.manageState(action)

    def handleEvent(self, event):
      # attempt to manage state based on keypresses
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            self._movement[pygame.K_LEFT] = True
            self._FSM.manageState("left")
         elif event.key == pygame.K_RIGHT:
            self._movement[pygame.K_RIGHT] = True
            self._FSM.manageState("right")
            # Check for jumping keypress
         elif event.key == pygame.K_UP:
            self._movement[pygame.K_UP] = True
            self._FSM.manageState("jump")
         elif event.key == pygame.K_DOWN:
            self._movement[pygame.K_DOWN] = True
            self._FSM.manageState("duck")

    def update(self, worldInfo, ticks):
        newPosition = self._position
        if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
            self._velocity.x = -self._velocity.x
        super().update(ticks)
        #scale velocity if magnitude exceeds max
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)
        #self._forcefield.update(worldInfo, ticks, self._velocity)
        # decrease the jump timer by ticks
        if self._FSM == "jumping":
            self._jumpTimer += ticks

            if self._jumpTimer > self._jumpTime:
                self._FSM.manageState("fall")
        elif self._FSM == "grounded" or self._FSM == "platformed":
            self._jumpTimer = 0
