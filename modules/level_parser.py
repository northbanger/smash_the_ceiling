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

CHAR_SPRITE_SIZE = Vector2(32, 32)

class LevelParser:
    def __init__(self, filename):
        self._filename = filename
        self._decorations = []
        self._platforms = []
        self._traps = {"bra":[], "pan":[], "ring":[]}
        self._enemies = {"devil":[], "gaston": []}

    def loadLevel(self):
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.plantFlowers()
        self.getPlatforms(fileContents)
        self.getTraps(fileContents)
        self.getEnemies(fileContents)

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
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "platform":
                for i in range(int(info[3])):
                    self._platforms.append(Drawable("platform.png", Vector2(int(info[1]) + 50*i, int(info[2])), (0,0)))

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



def main():
    parser = LevelParser("level1.txt")
    parser.loadLevel()

if __name__ == "__main__":
   main()
