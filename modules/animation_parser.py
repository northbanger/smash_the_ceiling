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

SCREEN_SIZE = [320,320]
SCALE = 2
SCALE2 = 1.25
UPSCALED = [int(x * SCALE2) for x in SCREEN_SIZE]

class AnimationParser:
    def __init__(self, filename):
        self._filename = filename
        self._background = Drawable(self.getBackground(), Vector2(0,0), (0,0))
        self._worldsize = (400, 400)
        self._text = []
        self._animationTimer = 0
        self._animationTime = 20
        self._ready = False

    def getBackground(self):
        if self._filename == "smash1.txt":
            backgroundImage = "background.png"
        elif self._filename == "smash2.txt":
            backgroundImage = "background2.png"
        return backgroundImage

    def loadAnimation(self):
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.getWorldSize(fileContents)
        self.getText(fileContents)

    def reset(self):
        self._text = []
        self._animationTimer = 0

    def getText(self, fileContents):
        fileStuff = fileContents.split("\n")
        #text,xval,yval,words
        #line 0 starts at A (first letter): ascii 65
        #lint 1 starts at N (13th letter)
        selectionCount = 0
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "text":
                text = info[3].upper()
                xCenter = (self._worldsize[0] + int(info[1]))/2 - (len(text)//2 * 11)
                for i in range(len(text)):
                    if text[i] != " ":
                        aVal = ord(text[i])
                        numInAlph = aVal - 65
                        offsetY = numInAlph // 13
                        offsetX = numInAlph - 13*offsetY
                        self._text.append(Drawable("font.png", Vector2(int(xCenter) + 8 * i, int(info[2])), (2 + offsetX, 7 + offsetY)))

    def getWorldSize(self,fileContents):
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "world size":
                self._worldsize = (int(info[1]), int(info[2]))

    def draw(self, screen):
        drawSurface = pygame.Surface(SCREEN_SIZE)
        self._background.draw(drawSurface)
        #self._background.draw(screen)
        #for letter in self._text:
        #    letter.draw(screen)
        for letter in self._text:
            #letter.draw(screen)
            letter.draw(drawSurface)
        pygame.transform.scale(drawSurface,UPSCALED,screen)

    def nextLevel(self):
        return self._ready

    def update(self, ticks):
        self._animationTimer += ticks
        if self._animationTimer > self._animationTime:
            self._ready = True
