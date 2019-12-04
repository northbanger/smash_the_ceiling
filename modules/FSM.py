"""
Author: Professor Matthews
Eidted by: Abby Nason
smash! the ceiling
FSM.py

Creates a FSM object.
"""

class FSM(object):
   def __init__(self, state="falling"):
      self._state = state
      self._facing = "none"



   def manageState(self, action):
      # Only change direction if we are facing "none"
      if action in ["left", "right"] and self._facing == "none":
         self._setFacing(action)

      # Face nothing if we stop
      elif action == "stopMoving":
         self._setFacing("none")

      # If we "collideGround" and are "falling", change to "grounded"
      elif action == "collideGround" and self._state == "falling":
          self._setState("grounded")

      # If the new action is "jump" and we not "falling", change state to "jumping"
      elif action == "jump" and self._state != "falling":
          self._setState("jumping")

      # If the new state is "fall" and we are "jumping", change state to "falling"
      elif action == "fall" and self._state == "jumping":
          self._setState("falling")

      # If the new state is "duck" and we are not "jumping" or "falling", change state to "ducking"
      elif action == "duck" and self._state != "jumping" and self._state != "falling":
          self._setState("ducking")

      # If the new state is "duck" and we are "falling", change state to "falling"
      elif action == "duck" and self._state == "falling":
          self._setState("falling")

      # If the new state is "duck" and we are "jumping", change state to "jumping"
      elif action == "duck" and self._state == "jumping":
          self._setState("jumping")

      # If the new state is "collideGround" and we are "ducking", change state to "grounded"
      elif action =="collideGround" and self._state == "ducking":
          self._setState("grounded")

      # If the new state is "fall" and we are "platformed", change state to "falling"
      elif action == "fall" and self._state == "platformed":
          #print("here")
          self._setState("falling")

      # If the new state is "collidePlatform" and we are "falling" or "ducking", change state to "platoform"
      elif action == "collidePlatform" and (self._state == "falling" or self._state == "ducking"):
          self._setState("platformed")


   def _setFacing(self, direction):
      self._facing = direction



   def _setState(self, state):
      self._state = state


   def isFacing(self, facing):
      """return the direction we are facing"""
      return self._facing == facing

   def isFalling(self):
       """return if we are falling"""
       return self._state == "falling"

   def isJumping(self):
       """return if we are jumping"""
       return self._state == "jumping"

   def isGrounded(self):
       """return if we are grounded"""
       return self._state == "grounded"

   def isDucking(self):
       """return if we are ducking"""
       return self._state == "ducking"

   def isPlatformed(self):
       """return if we are platformed"""
       return self._state == "platformed"

   def __eq__(self, state):
      return self._state == state
