

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

      # If the new state is "fall" and we are "jumping, change state to "falling"
      elif action == "fall" and self._state == "jumping":
          self._setState("falling")

      elif action == "duck" and self._state != "jumping" and self._state != "falling":
          self._setState("ducking")

      elif action == "duck" and self._state == "falling":
          self._setState("falling")

      elif action =="collideGround" and self._state == "ducking":
          self._setState("grounded")


   def _setFacing(self, direction):
      self._facing = direction



   def _setState(self, state):
      self._state = state


   def isFacing(self, facing):
      return self._facing == facing

   def isFalling(self):
       return self._state == "falling"

   def isJumping(self):
       return self._state == "jumping"

   def isGrounded(self):
       return self._state == "grounded"

   def isDucking(self):
       return self._state == "ducking"

   def __eq__(self, state):
      return self._state == state
