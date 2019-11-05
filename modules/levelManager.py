from .utils.vector2D import Vector2
from .utils.backgrounds import RepeatingBackground
from .utils.drawable import Drawable
from .star import Star
from pygame import Rect, KEYDOWN, K_SPACE
import os


class LevelManager(object):
   _WORLD_SIZE = Vector2(2400, 400)

   def __init__(self, filename):
      self._background = Drawable("background.png", Vector2(0,0), (0,0))
      file = open(os.path.join("resources", "levels", filename))
      fileContents = file.read()
      file.close()
      #starPosition = fileContents.split(',')
      self._blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))
      print(starPosition)

   def draw(self, surface):
      surface.fill((30,30,30))
      self._background.draw(surface)
      #background.draw(screen)
      #ground.draw(screen)
      #for platform2 in platforms:
        #  platform2.draw(screen)
      #for trap2 in traps:
        #  trap2.draw(screen)
      #blob.draw(screen)
      self._star.draw(surface)

   def handleEvent(self, event):

      if event.type == KEYDOWN and event.key == K_SPACE:
         return True

      self._blob.handleEvent(event)

   def update(self, ticks, screenSize):
      for trap3 in traps:
          if trap3.ranInto():
              if trap3 == bra:
                  traps.remove(trap3)
              elif trap3 == pan:
                  trap.resetRanInto()
      clipRect = blob.getCollideRect().clip(ground.getCollideRect())

      if clipRect.width > 0:
         blob.manageState("collideGround")

      #variable to determine if already collided with a platform
      i = True
      blobPos = blob.getCollideRect()
      for platform in platforms:
          platPos = platform.getCollideRect()
          print(platPos)
          clipRect2 = blobPos.clip(platPos)
          print(clipRect2.width > 0)
          print(blob._FSM._state)
          print(blobPos[1] - 90)
          print(platPos[1] + platPos[3])
          print()
          #if clipRect2.width > 0 and blob._FSM == "jumping" and blobPos[1] - 10 <= platPos[1] + platPos[3]:
        #      blob.manageState("fall")
          if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
              blob._velocity.x = -blob._velocity.x
              blob._velocity.y = -blob._velocity.y
              blob.manageState("fall")
          elif clipRect2.width >= 5 and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
              blob.manageState("collidePlatform")
              i = False
          elif clipRect2.width < 5 and blob._FSM == "platformed" and i:
              print("FALL")
              blob.manageState("fall")
              blob.updateVisual()

      for trap in traps:
          if blob.getCollideRect().colliderect(trap.getCollideRect()):
              trap.handleCollision()
              if trap == bra:
                  blob._velocity.x = -blob._velocity.x
              elif trap == pan:
                  blob._velocity.x = -blob._velocity.x * 0.5
                  blob._velocity.y = -blob._velocity.y
      self._blob.update(ticks, LevelManager._WORLD_SIZE)
      for pan in pans:
          pan.update(ticks)
      Drawable.updateWindowOffset(self._star, screenSize, LevelManager._WORLD_SIZE)
