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

    def getBackground(self):
        if self._filename == "level1.txt":
            backgroundImage = "background.png"
        if self._filename == "level2.txt":
            backgroundImage = "background2.png"
        return backgroundImage

    def getGround(self):
        if self._filename == "level1.txt":
            groundImage = "ground2.png"
        if self._filename == "level2.txt":
            groundImage = "ground3.png"
        return groundImage

    def loadLevel(self):
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
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

    def plantFlowers(self):
        flowerSize = 16
        for xPos in range(0, 2400, 20):
            randomNumber = random.randint(10,13)
            self._decorations.append(Drawable("nuts_and_milk.png", Vector2(xPos, 300-flowerSize), (randomNumber,8)))

    def getPlatforms(self, fileContents):
        if self._filename == "level1.txt":
            print("level1")
            platformImage = "platform.png"
            print("level2")
        elif self._filename == "level2.txt":
            platformImage = "platform2.png"
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "platform":
                for i in range(int(info[3])):
                    self._platforms.append(Drawable(platformImage, Vector2(int(info[1]) + 50*i, int(info[2])), (0,0)))
        #print(len(self._platforms))

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
        for back in self._elevator._parts["back"]:
            back.draw(screen)
        self._blob.draw(screen)
        for zap in self._blob._zaps:
            if zap.isActive():
                zap.draw(screen)
            elif zap.notActive() > 5:
                self._blob._zaps.remove(zap)
            else:
                zap.incNotActive()
                zap.draw(screen)
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
                elif zappy.notActive() > 5:
                    gas._arrows.remove(arrow15)
                else:
                    arrow15.incNotActive()
                    arrow15.draw(screen)




def main():
    parser = LevelParser("level1.txt")
    parser.loadLevel()

if __name__ == "__main__":
   main()
