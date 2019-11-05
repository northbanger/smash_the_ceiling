from .UI.pauser import Pauser
from .levelManager import LevelManager
from .FSMs.gameFSM import GameState

class GameManager(object):

   def __init__(self, screenSize):
      self._pauser = Pauser(screenSize)
      self._level = LevelManager("level1.txt")
      self._FSM = GameState()

      self._currentLevel = 1


   def draw(self, surface):
      if self._FSM in ["paused", "running"]:
         self._level.draw(surface)
      if self._FSM == "paused":
         self._pauser.draw(surface)


   def handleEvent(self, event):
      if self._FSM == "paused":
         self._pauser.handleEvent(event)

         if not self._pauser.isActive():
            self._FSM.manageState("unpause")

      elif self._FSM == "running":
         self._pauser.handleEvent(event)

         if self._pauser.isActive():
            self._FSM.manageState("pause")
         else:
            levelDone = self._level.handleEvent(event)

            if levelDone:
               self._FSM.manageState("nextLevel")



   def update(self, ticks, screenSize):
      if self._FSM == "running":
         levelDone = self._level.update(ticks, screenSize)

         if levelDone:
            self._FSM.manageState("nextLevel")

      elif self._FSM == "startLoading":
         self._currentLevel += 1

         if self._currentLevel == 4:
             self._currentLevel = 1

         self._level = LevelManager("level" + str(self._currentLevel) + ".txt")
         self._FSM.manageState("doneLoading")

         print("Level", self._currentLevel)
