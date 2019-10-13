import pygame
from .mobile import Mobile
from .FSM import FSM
from .vector2D import Vector2

class Jumper(Mobile):
   def __init__(self):
      self._jumpTimer = 0
      self._jumpTime = 0.5
      self._vSpeed = 100
      self._jSpeed = 100

   # Public access to tell jumper to try to take some action, typically for collision
   def manageState(self, action):
      self._FSM.manageState(action)

   def handleEvent(self, event):
      # attempt to manage state based on keypresses
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_a:
            self._FSM.manageState("left")
         elif event.key == pygame.K_d:
            self._FSM.manageState("right")
            # Check for jumping keypress
         elif event.key == pygame.K_w:
            self._FSM.manageState("jump")
      elif event.type == pygame.KEYUP:
         if event.key in [pygame.K_a, pygame.K_d]:
            self._FSM.manageState("stopMoving")
        # check for release of jumping keypress
         elif event.key == pygame.K_w:
            self._FSM.manageState("fall")

   def update(self, ticks):
      super().update(ticks)
      # decrease the jump timer by ticks
      if self._FSM == "jumping":
          self._jumpTimer += ticks

          if self._jumpTimer > self._jumpTime:
              self._FSM.manageState("fall")
      elif self._FSM == "grounded":
          self._jumpTimer = 0


      # check if the jump timer is over and transition to falling if so
