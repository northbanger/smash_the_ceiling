import pygame
import os
import random
from modules.vector2D import Vector2
from characters.bra import Bra
from characters.pan import Pan
from characters.ring import Ring
from characters.devil import Devil
from characters.gaston import Gaston
from modules.drawable import Drawable
from characters.blob import Blob
from characters.elevator import Elevator
from characters.ceiling import Ceiling

CHAR_SPRITE_SIZE = Vector2(32, 32)

class LevelParser:
    def __init__(self, filename):
        self._filename = filename
        self._background = Drawable(self.getBackground(), Vector2(0,0), (0,0))
        self._ground = Drawable(self.getGround(), Vector2(0, 300), (0,0))
        self._blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))
        self._decorations = []
        self._platforms = []
        self._traps = {"bra":[], "pan":[], "ring":[]}
        self._enemies = {"devil":[], "gaston": []}
        self._worldsize = (2400, 400)
        self._elevator = elevator = Elevator(Vector2(self._worldsize[0]-50,300), self._worldsize[1])
        self._ceiling = Ceiling(Vector2(0, 0), final=False)
        self._deathCycle = 0
        self._keydown = {1:False, 2:False, 3:False}

    def getBackground(self):
        if self._filename == "level1.txt":
            backgroundImage = "background.png"
        elif self._filename == "level2.txt":
            backgroundImage = "background2.png"
        elif self._filename == "level3.txt":
            backgroundImage = "background3b.png"
        elif self._filename == "level4.txt":
            backgroundImage = "background4.png"
        return backgroundImage

    def getGround(self):
        if self._filename == "level1.txt":
            groundImage = "ground2.png"
        elif self._filename == "level2.txt":
            groundImage = "ground3.png"
        elif self._filename == "level3.txt":
            groundImage = "ground4b.png"
        elif self._filename == "level4.txt":
            groundImage = "ground5.png"
        return groundImage

    def loadLevel(self):
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.getWorldSize(fileContents)
        self._ground = Drawable(self.getGround(), Vector2(0, self._worldsize[1]-100), (0,0))
        self._blob = Blob(Vector2(0,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y), color=self._blob._color)
        self.plantFlowers()
        self.getPlatforms(fileContents)
        self.getTraps(fileContents)
        self.getEnemies(fileContents)
        self.getWorldSize(fileContents)

    def reset(self):
        self._decorations = []
        self._platforms = []
        self._traps = {"bra":[], "pan":[], "ring":[]}
        self._enemies = {"devil":[], "gaston": []}
        self._deathCycle = 0
        self._keydown = {1:False, 2:False, 3:False}

    def plantFlowers(self):
        flowerSize = 16
        for xPos in range(0, 2400, 20):
            randomNumber = random.randint(10,13)
            self._decorations.append(Drawable("nuts_and_milk.png", Vector2(xPos, self._worldsize[1]-100-flowerSize), (randomNumber,8)))

    def getPlatforms(self, fileContents):
        if self._filename == "level1.txt":
            platformImage = "platform.png"
        elif self._filename == "level2.txt":
            platformImage = "platform2.png"
        elif self._filename == "level3.txt":
            platformImage = "platform3.png"
        elif self._filename == "level4.txt":
            platformImage = "platform4.png"
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "platform":
                for i in range(int(info[3])):
                    self._platforms.append(Drawable(platformImage, Vector2(int(info[1]) + 50*i, int(info[2])), (0,0)))

    def getTraps(self, fileContents):
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "trap":
                if info[1] == "bra":
                    self._traps[info[1]].append(Bra(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
                elif info[1] == "ring":
                    self._traps[info[1]].append(Ring(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
                elif info[1] == "pan":
                    self._traps[info[1]].append(Pan(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))

    def getEnemies(self, fileContents):
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "enemy":
                if info[1] == "devil":
                    self._enemies[info[1]].append(Devil(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y), int(info[4])))
                elif info[1] == "gaston":
                    self._enemies[info[1]].append(Gaston(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))

    def getWorldSize(self,fileContents):
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "world size":
                self._worldsize = (int(info[1]), int(info[2]))

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_1:
               self._keydown[1] = True
           if event.key == pygame.K_2:
               self._keydown[2] = True
           if event.key == pygame.K_3:
               self._keydown[3] = True
        elif event.type == pygame.KEYUP:
           if event.key == pygame.K_1:
               self._keydown[1] = False
           if event.key == pygame.K_2:
               self._keydown[2] = False
           if event.key == pygame.K_3:
               self._keydown[3] = False
        self._blob.handleEvent(event)

    def draw(self, screen):
        self._background.draw(screen)
        self._ground.draw(screen)
        for decoration in self._decorations:
            decoration.draw(screen)
        for platform2 in self._platforms:
            platform2.draw(screen)
        for category2 in self._traps:
            for trap2 in self._traps[category2]:
                trap2.draw(screen)
        for category10 in self._enemies:
            for enemy10 in self._enemies[category10]:
                enemy10.draw(screen)
        if self._filename != "level3.txt":
            for back in self._elevator._parts["back"]:
                back.draw(screen)
        if self._filename == "level3.txt":
            self._ceiling.draw(screen)
        self._blob.draw(screen)
        for zap in self._blob._zaps:
            if zap.isActive():
                zap.draw(screen)
            elif zap.notActive() > 5:
                self._blob._zaps.remove(zap)
            else:
                zap.incNotActive()
                zap.draw(screen)
        if self._filename != "level3.txt":
            for part in self._elevator._parts:
                if part != "back":
                    for section in self._elevator._parts[part]:
                        section.draw(screen)
        #elevator.draw(screen)
        if self._blob._forcefield.isActive():
            self._blob._forcefield.draw(screen)
        for ringy in self._traps["ring"]:
            for zappy in ringy._zaps:
                if zappy.isActive():
                    zappy.draw(screen)
                elif zappy.notActive() > 5:
                    ringy._zaps.remove(zappy)
                else:
                    zappy.incNotActive()
                    zappy.draw(screen)
        for gas in self._enemies["gaston"]:
            for arrow15 in gas._arrows:
                if arrow15.isActive():
                    arrow15.draw(screen)
                elif arrow15.notActive() > 5:
                    gas._arrows.remove(arrow15)
                else:
                    arrow15.incNotActive()
                    arrow15.draw(screen)

    def detectCollision(self):
         for category3 in self._traps:
            for trap3 in self._traps[category3]:
                if trap3.ranInto():
                    if category3 == "bra":
                        self._traps[category3].remove(trap3)
                    elif category3 == "pan":
                        trap3.resetRanInto()

         #variable to determine if already collided with a platform
         clipRect = self._blob.getCollideRect().clip(self._ground.getCollideRect())

         if clipRect.width > 0:
            self._blob.manageState("collideGround")

         i = True
         blobPos = self._blob.getCollideRect()
         totalClipWidth = 0
         if self._filename == "level3.txt":
             if self._blob._position.y <= 25:
                 self._blob.manageState("fall")
                 if self._blob._velocity.y < 0:
                     self._blob._velocity.y = -self._blob._velocity.y
                     if self._blob._position.x <= 200:
                         self._ceiling.incHP("left")
                     elif self._blob._position.x > 200:
                         self._ceiling.incHP("right")
                 self._ceiling.updateVisual()
         for platform in self._platforms:
             platPos = platform.getCollideRect()
             clipRect2 = blobPos.clip(platPos)
             totalClipWidth += clipRect2.width
             if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
                 if blobPos[0] < platPos[0] and self._blob._velocity.x >= 0:
                     if self._blob._velocity.x == 0:
                         self._blob._velocity.x = -100
                     else:
                         self._blob._velocity.x = -self._blob._velocity.x
                 elif blobPos[0] + blobPos[2] > platPos[0] + platPos[2] and self._blob._velocity.x <= 0:
                     if self._blob._velocity.x == 0:
                         self._blob._velocity.x = 100
                     else:
                         self._blob._velocity.x = -self._blob._velocity.x
                 if self._blob._velocity.y <= 0:
                     self._blob._velocity.y = -self._blob._velocity.y
                 self._blob.manageState("fall")
             elif (clipRect2.width >= 5 or (clipRect2.width > 0 and totalClipWidth == 32)) and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
                 self._blob.manageState("collidePlatform")
                 i = False
             elif clipRect2.width < 5 and self._blob._FSM == "platformed" and i:
                 self._blob.manageState("fall")
                 self._blob.updateVisual()

         for category in self._traps:
             for trap in self._traps[category]:
                 if self._blob.getCollideRect().colliderect(trap.getCollideRect()):
                     trap.handleCollision()
                     if category == "bra":
                         self._blob._velocity.x = -self._blob._velocity.x
                         if not self._blob._forcefield.isActive():
                             self._blob.die()
                     elif category == "pan":
                         self._blob._velocity.x = -self._blob._velocity.x * 0.5
                         self._blob._velocity.y = -self._blob._velocity.y
                         if not self._blob._forcefield.isActive():
                             self._blob.die()
                     elif category == "ring":
                         if blobPos[0] + blobPos[2] > trap.getCollideRect()[0] + trap.getCollideRect()[2]:
                             self._blob._velocity.x = 100
                         else:
                             self._blob._velocity.x = -100
                         self._blob._velocity.y = -self._blob._velocity.y

         for category4 in self._traps:
             for trap4 in self._traps[category4]:
                 for zap4 in self._blob._zaps:
                     if zap4.getCollideRect().colliderect(trap4.getCollideRect()):
                         if category4 == "bra":
                             trap4.handleCollision()
                             zap4.handleDestroy()
                         if category4 == "pan":
                             self._traps[category4].remove(trap4)
                             zap4.handleDestroy()
                         elif category4 == "ring":
                              zap4.handleEnd()

         for category17 in self._enemies:
             for enemy17 in self._enemies[category17]:
                 for zap17 in self._blob._zaps:
                     if zap17.getCollideRect().colliderect(enemy17.getCollideRect()):
                         enemy17.handleCollision()
                         zap17.handleDestroy()
                         if enemy17.isDead() and enemy17 in self._enemies[category17]:
                             self._enemies[category17].remove(enemy17)

         for category21 in self._enemies:
             for enemy21 in self._enemies[category21]:
                 if self._blob.getCollideRect().colliderect(enemy21.getCollideRect()):
                     self._blob._velocity.x = -self._blob._velocity.x
                     if category21 == "devil":
                         if not self._blob._forcefield.isActive():
                             self._blob.die()

         for ring7 in self._traps["ring"]:
             for ringZap in ring7._zaps:
                 for blobZap in self._blob._zaps:
                     if ringZap.getCollideRect().colliderect(blobZap.getCollideRect()):
                         ringZap.handleDestroy()
                         blobZap.handleDestroy()

         for gaston50 in self._enemies["gaston"]:
             for arrow50 in gaston50._arrows:
                 for blobZap50 in self._blob._zaps:
                     if arrow50.getCollideRect().colliderect(blobZap50.getCollideRect()):
                         arrow50.handleDestroy()
                         blobZap50.handleDestroy()

         if self._blob._forcefield.isActive():
             for ring40 in self._traps["ring"]:
                 for ringZap40 in ring40._zaps:
                     if ringZap40.getCollideRect().colliderect(self._blob._forcefield.getCollideRect()):
                         ringZap40.handleDestroy()

             for gaston82 in self._enemies["gaston"]:
                 for arrow82 in gaston82._arrows:
                     if arrow82.getCollideRect().colliderect(self._blob._forcefield.getCollideRect()):
                         arrow82.handleDestroy()

         for ring20 in self._traps["ring"]:
             for zap20 in ring20._zaps:
                 if zap20.getCollideRect().colliderect(self._blob.getCollideRect()):
                     zap20.handleDestroy()
                     if not self._blob._forcefield.isActive():
                         self._blob.die()

         for gaston64 in self._enemies["gaston"]:
             for arrow64 in gaston64._arrows:
                 if arrow64.getCollideRect().colliderect(self._blob.getCollideRect()):
                     arrow64.handleDestroy()
                     if not self._blob._forcefield.isActive():
                         self._blob.die()

         for door in self._elevator._parts["doors"]:
             for zap102 in self._blob._zaps:
                 if zap102.getCollideRect().colliderect(door.getCollideRect()):
                     zap102.handleEnd()

         for platform3 in self._platforms:
             for zap5 in self._blob._zaps:
                 if zap5.getCollideRect().colliderect(platform3.getCollideRect()):
                     zap5.handleEnd()
             for ring15 in self._traps["ring"]:
                 for zap15 in ring15._zaps:
                     if zap15.getCollideRect().colliderect(platform3.getCollideRect()):
                         zap15.handleEnd()

    def update(self, WORLD_SIZE, SCREEN_SIZE, ticks):
        if self._keydown[1] == True and self._keydown[2] == True and self._keydown[3] == True:
            if self._filename != "level3.txt":
                self._blob.update(WORLD_SIZE, ticks, cheat=True, horizontal=True)
            else:
                self._blob.update(WORLD_SIZE, ticks, cheat=True, horizontal=False)
        else:
            self._blob.update(WORLD_SIZE, ticks)
        for pan in self._traps["pan"]:
            pan.update(ticks)
        for zap2 in self._blob._zaps:
            zap2.update(WORLD_SIZE, ticks)
        for devil in self._enemies["devil"]:
            devil.update(WORLD_SIZE, ticks)
        for gaston in self._enemies["gaston"]:
            gaston.update(WORLD_SIZE, ticks)
        for ring in self._traps["ring"]:
            ring.update(WORLD_SIZE, ticks)

        if self._blob.isDead():
            if self._deathCycle > 30:
                self.reset()
                self.loadLevel()
                # initialize the blob on top of the ground
                self._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y), self._blob._color)
                self._deathCycle = 0
            self._deathCycle += 1



        # getting the offset of the of the star (our tracking object)
        Drawable.updateOffset(self._blob, SCREEN_SIZE, WORLD_SIZE)




def main():
    parser = selfParser("level1.txt")
    parser.loadLevel()

if __name__ == "__main__":
   main()
