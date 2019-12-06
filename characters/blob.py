"""
Abby Nason
smash! the ceiling
blob.py

Creates a blob, which is our hero.
"""

import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
from characters.blobzap import BlobZap
from modules.frameManager import FRAMES
import os
from modules.soundManager import SoundManager

SPRITE_SIZE = Vector2(32, 32)
MAX_VELOCITY = 155 #150
ACCELERATION = 6.5 #5.0
STANDARD_JUMP = 0.75

class Blob(Mobile):
    """creates a blob"""
    def __init__(self, position, color="pink"):
        """initializes a blob object"""
        self._color = color
        #determines which blob image to grab based on the color
        if color == "pink":
            self._offset = (0,0)
        elif color == "blue":
            self._offset = (1,0)
        elif color == "green":
            self._offset = (2,0)
        elif color == "orange":
            self._offset = (3,0)
        super().__init__("blobs.png", position, self._offset)
        #a vector2 of its velocity
        self._velocity = Vector2(0,0)
        self._maxVelocity = MAX_VELOCITY
        self._acceleration = ACCELERATION
        self._movement = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        self._jumpTimer = 0
        self._jumpTime = STANDARD_JUMP
        self._vSpeed = 100
        self._jSpeed = 80
        self._zaps = []
        self._alive = True
        self._forcefield = False
        self._forcefieldTime = 5
        self._forcefieldTimer = 0
        self._higher = False
        self._highTime = 10
        self._highTimer = 0
        self._endLevel = False

    def manageState(self, action):
      """tells blob which action to take"""
      self._FSM.manageState(action)

    def die(self):
      """kills the blob"""
      self._alive = False

    def isDead(self):
      """returns if blob is dead or not"""
      return not self._alive

    def activateForcefield(self):
        """returns if forcefield is active"""
        self._forcefield = True

    def increaseJumpTime(self):
        """temporarily increases the jump time"""
        self._higher = True
        self._jumpTime = 1.5

    def moveForward(self, levelFile):
        """teleports blob forward if level is horizontal and upward if
        level is vertical"""
        if levelFile != "level3.txt" and levelFile != "level6.txt":
            self._position.x += 200

        else:
            self._position.x = 0
            self._position.y -= 200

    def handleEvent(self, event):
      """manage state based on key presses"""
      #arrow keys to move and spacebar to spawn a zap
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
            self.updateVisual()
         elif event.key == pygame.K_SPACE:
            if self._FSM.isFacing("left"):
                zap = BlobZap(Vector2(self._position.x - SPRITE_SIZE.x, self._position.y + SPRITE_SIZE.y//2 - 6))
            else:
                zap = BlobZap(Vector2(self._position.x + SPRITE_SIZE.x, self._position.y + SPRITE_SIZE.y//2 - 6))
            self._zaps.append(zap)
            SoundManager.getInstance().playSound("heart.ogg")
            zap.handleEvent(self._FSM.isFacing("left"))

      elif event.type == pygame.KEYUP:
         if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            if event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = False
            if event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = False
            self._FSM.manageState("stopMoving")
        # check for release of jumping keypress
         elif event.key == pygame.K_UP:
            self._movement[pygame.K_UP] = False
            self._FSM.manageState("fall")
         elif event.key == pygame.K_DOWN:
            self._movement[pygame.K_DOWN] = False
            if self._position.y + 32 >= 300:
                self._FSM.manageState("collideGround")
            else:
                self._FSM.manageState("collidePlatform")
            self.updateVisual()

    def handleEndLevel(self):
        """tells blob it is time to go up in the elevator"""
        self._endLevel = True

    def update(self, worldInfo, ticks, cheat=False, horizontal=False):
        """update the blob based on movement, animation, if a cheat has been
        used and the orientation of the level"""
        #forcefield active
        if self._forcefield == True:
            self._forcefieldTimer += ticks
            if self._forcefieldTimer > self._forcefieldTime:
                self._forcefieldTimer = 0
                self._forcefield = False
            self.updateVisual()
        #higher jumps active
        if self._higher == True:
            self._highTimer += ticks
            if self._highTimer > self._highTime:
                self._highTimer = 0
                self._jumpTime = STANDARD_JUMP
                self._higher = False
            self.updateVisual()

        #no cheat used
        if not cheat:
            #not the end of the level
            if not self._endLevel:
                newPosition = self._position
                if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
                    self._velocity.x = -self._velocity.x
                super().update(ticks)
                #scale velocity if magnitude exceeds max
                if self._velocity.magnitude() > self._maxVelocity:
                    self._velocity.scale(self._maxVelocity)
                #self._forcefield.update(worldInfo, ticks)
                # decrease the jump timer by ticks
                if self._FSM == "jumping":
                    self._jumpTimer += ticks

                    if self._jumpTimer > self._jumpTime:
                        self._FSM.manageState("fall")
                elif self._FSM == "grounded" or self._FSM == "platformed":
                    self._jumpTimer = 0
                    self.updateVisual()
            else:
                #elevator transition
                self._position.y -= 5
                self._velocity.x = 0
                self._velocity.y = -MAX_VELOCITY//8 * ticks
                if self._velocity.magnitude() > self._maxVelocity:
                    self._velocity.scale(self._maxVelocity)
                #super().update(ticks)
        else:
            #cheat used -- different for horizontal vs. vertical
            if horizontal and self._position.x < 1950:
                self._position.x = 1950
                self._position.y = 300 - 32
            elif not horizontal and self._position.y > 70:
                self._position.x = 50
                self._position.y = 70


    def updateVisual(self, inactive=False):
        """update the image of the blob depending on state and if powerups are active"""
        #if forcefield is active grab images that have the forcefield on them
        if inactive:
            self._image = FRAMES.getFrame(self._imageName, (self._offset[0],0))
        else:
            if self._forcefield:
                fullImage = pygame.image.load(os.path.join("images", "blobs_forcefield.png")).convert()
                #if self._FSM.isDucking():
                #    y = 1
                if self._FSM.isJumping() or self._FSM.isFalling():
                    y = 2
                else:
                    y = 0
                self._image = FRAMES.getFrame("blobs.png", (self._offset[0],y))
            else:
                #otherwise grab the normal images
                fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
                #if in air
                if self._FSM.isJumping() or self._FSM.isFalling():
                    y = 2
                #if dead and grounded
                elif self._FSM.isGrounded() and not self._alive:
                    y = 1
                else:
                    #if normal on ground or platformed
                    y = 0
                self._image = FRAMES.getFrame(self._imageName, (self._offset[0],y))
