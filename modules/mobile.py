
from .drawable import Drawable
from .vector2D import Vector2
from .FSM import FSM

TERM_VEL = 50

class Mobile(Drawable):
   def __init__(self, imageName, position, rect=None):
      super().__init__(imageName, position, rect)
      self._velocity = Vector2(0,0)
      self._gravity = 100

      self._FSM = FSM()


   def update(self, ticks):

      newPosition = self.getPosition()

      # Set horizontal velocity based on the current facing
      if not self._FSM.isFacing("none"):
         if self._FSM.isFacing("left"):
            if not (self._FSM.isJumping() or self._FSM.isFalling()):
                self._velocity[0] -= self._vSpeed * ticks
         elif self._FSM.isFacing("right"):
            if not (self._FSM.isJumping() or self._FSM.isFalling()):
                self._velocity[0] += self._vSpeed * ticks

      else:
         if abs(self._velocity[0]) > 0:
            self._velocity[0] /= 2
            if abs(self._velocity[0]) < 0.01:
               self._velocity[0] = 0


      # Set vertical velocity based on jumping/falling states
      if self._FSM.isJumping():
          self._velocity[1] = -self._jSpeed

      elif self._FSM.isFalling():
          self._velocity[1] += self._gravity * ticks

      elif self._FSM.isGrounded():
          self._velocity[1] = 0

      elif self._FSM.isDucking():
          self._velocity[1] = 0

      elif self._FSM.isPlatformed():
          self._velocity[1] = 0


      # Update position based on velocity
      newPosition += self._velocity * ticks

      self.setPosition(newPosition)
