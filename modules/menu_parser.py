"""
Abby Nason
smash! the ceiling
menu_parser.py

Parses the menu layout file and creates the level.
"""

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
SCREEN_SIZE = [160,160]
SCALE = 2
SCALE2 = 2.5
UPSCALED = [int(x * SCALE2) for x in SCREEN_SIZE]

class MenuParser:
    def __init__(self, filename):
        """intializes a menu"""
        self._filename = filename
        self._background = Drawable(self.getBackground(), Vector2(0,0), (0,0))
        self._accent = Drawable("menu_accent.png", Vector2(0,45), (0,0))
        self._worldsize = (400, 400)
        self._selectionAreas = []
        self._blobs = []
        self._text = []
        self._selectedBlob = None
        self._ready = False
        self._startButton = None

    def getBackground(self):
        """returns the appropriate background image"""
        if self._filename == "startmenu.txt":
            #backgroundImage = "background.png"
            backgroundImage = "background6.png"
        elif self._filename == "blobmenu.txt":
            #backgroundImage = "background2.png"
            backgroundImage = "background6.png"
        return backgroundImage

    def loadMenu(self):
        """controls the loading of the level"""
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.getWorldSize(fileContents)
        self.getBlobSelectionAreas(fileContents)
        self.getStartButton(fileContents)
        self.getText(fileContents)

    def reset(self):
        """resets a menu"""
        self._selectionAreas = []
        self._blobs = []
        self._text = []
        self._ready = False
        self._selectedBlob = None

    def getBlobSelectionAreas(self, fileContents):
        """loads in the selection areas for choosing a blob to play with on a menu"""
        SELECTION_SIZE = Vector2(112, 112)
        BLOB_SIZE = Vector2(64, 64)
        fileStuff = fileContents.split("\n")
        selectionCount = 0
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "selection":
                if self._filename == "blobmenu.txt":
                    self._selectionAreas.append(Drawable("blob_selection.png", Vector2(int(info[1]), int(info[2])), (selectionCount,0)))
                    blobXpos = int(info[1]) + SELECTION_SIZE.x//2 - BLOB_SIZE.x//2
                    blobYpos = int(info[2]) + SELECTION_SIZE.y//2  - BLOB_SIZE.y//2 - 14
                    self._blobs.append(Drawable("menu_blobs.png", Vector2(blobXpos, blobYpos), (selectionCount + 1,0)))
                    selectionCount += 1

    def getStartButton(self, fileContents):
        """creates a start button with the given position"""
        fileStuff = fileContents.split("\n")
        #selection,xval,yval
        selectionCount = 0
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "start":
                xPos = (self._worldsize[0] - int(info[1]))//2 - 64//2
                self._startButton = Drawable("startbutton.png", Vector2(xPos, int(info[2])), (0,0))


    def getText(self, fileContents):
        """gets the image for each letter in the text given in the layout file"""
        fileStuff = fileContents.split("\n")
        #text,xval,yval,words
        #line 0 starts at A (first letter): ascii 65
        #lint 1 starts at N (13th letter)
        selectionCount = 0
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "text":
                text = info[3].upper()
                #xCenter = (self._worldsize[0] + int(info[1]))/4 - (len(text)//2 * 8)
                if self._filename == "startmenu.txt":
                    xCenter = 10
                else:
                    xCenter = 15
                for i in range(len(text)):
                    if text[i] != " ":
                        if text[i] == "!":
                            self._text.append(Drawable("exclamation.png", Vector2(int(xCenter) + 8 * i, int(info[2])), (0,0)))
                        else:
                            aVal = ord(text[i])
                            numInAlph = aVal - 65
                            offsetY = numInAlph // 13
                            offsetX = numInAlph - 13*offsetY
                            self._text.append(Drawable("font.png", Vector2(int(xCenter) + 8 * i, int(info[2])), (2 + offsetX, 7 + offsetY)))

    def getWorldSize(self,fileContents):
        """parses the menu layout file for the world size (vertical or horizontal)"""
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "world size":
                self._worldsize = (int(info[1]), int(info[2]))

    def draw(self, screen):
        """draws everything in the menu"""
        drawSurface = pygame.Surface(SCREEN_SIZE)
        self._background.draw(drawSurface)
        #self._accent.draw(drawSurface)
        #upscale the text
        for letter in self._text:
            letter.draw(drawSurface)
        pygame.transform.scale(drawSurface,UPSCALED,screen)
        for area in self._selectionAreas:
            area.draw(screen)
        for blob in self._blobs:
            blob.draw(screen)
        self._startButton.draw(screen)

    def handleEvent(self, event):
         """handles a mouse click event"""
         if event.type == pygame.MOUSEBUTTONDOWN:
            #left click is 1
            if event.button == 1:
                self.detectSelectedArea(list([int(x/SCALE) for x in event.pos]))

    def detectSelectedArea(self, mousePos):
        """determines which blob was selected based on the mouse position"""
        for area in self._selectionAreas:
            positionBox = area.getCollideRect()
            if positionBox.collidepoint(mousePos):
                if area == self._selectionAreas[0]:
                    color = "blue"
                elif area == self._selectionAreas[1]:
                    color = "green"
                elif area == self._selectionAreas[2]:
                    color = "orange"
                self._selectedBlob = color
                self._ready = False
        if self._startButton.getCollideRect().collidepoint(mousePos):
            self._ready = True


    def madeSelection(self):
        """determines if a blob has been selected before moving on
        to the next phase"""
        if self._filename == "startmenu.txt":
            self._selectedBlob = "pink"
            return True
        if self._selectedBlob != None:
            return True
        else:
            return False

    def getSelection(self):
        """return the selected blob to initialize the next level"""
        return self._selectedBlob

    def nextLevel(self):
        """return if the menu is ready for the next level"""
        return self._ready



def main():
    parser = MenuParser("blobmenu.txt")
    parser.loadMenu()


if __name__ == "__main__":
   main()
