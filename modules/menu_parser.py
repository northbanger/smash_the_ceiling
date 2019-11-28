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

class MenuParser:
    def __init__(self, filename):
        self._filename = filename
        self._background = Drawable(self.getBackground(), Vector2(0,0), (0,0))
        self._worldsize = (400, 400)
        self._selectionAreas = []
        self._blobs = []
        self._text = []

    def getBackground(self):
        if self._filename == "startmenu.txt":
            backgroundImage = "background.png"
        elif self._filename == "blobmenu.txt":
            backgroundImage = "background2.png"
        return backgroundImage

    def loadMenu(self):
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.getWorldSize(fileContents)
        self._ground = Drawable(self.getGround(), Vector2(0, self._worldsize[1]-100), (0,0))
        self._blob = Blob(Vector2(0,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y))
        self.getBlobSelectionAreas(fileContents)
        self.getText(fileContents)

    def reset(self):
        self._selectionAreas = []
        self._blobs = []
        self._text = []

    def getBlobSelectionAreas(self, fileContents):
        SELECTION_SIZE = Vector2(112, 112)
        BLOB_SIZE = Vector2(64, 64)
        fileStuff = fileContents.split("\n")
        #selection,xval,yval
        selectionCount = 0
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "selection":
                if self._filename == "blobmenu.txt":
                    self._selectionAreas.append(Drawable("blob_selection.png", Vector2(int(info[1]), int(info[2])), (selectionCount,0)))
                    blobXpos = (int(info[1]) + SELECTION_SIZE.x)/2 - BLOB_SIZE.x/2
                    blobYpos = (int(info[2]) + SELECTION_SIZE.y)/2  - BLOB_SIZE.y/2
                    self._blobs.append(Drawable("menu_blobs.png", Vector2(blobXpos, blobYpos), (selectionCount,0)))
                    selectionCount += 1

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
                for i in range(len(text)):
                    aVal = ord(text[i])
                    numInAlph = aVal - 65
                    offsetX = numInAlph // 13
                    offsetY = numInAlph - 13*offsetX
                    self._text.append(Drawable("font.png", Vector2(int(info[1]) + 8 * i, int(info[2])), (offsetX,offsetY)))

    def getWorldSize(self,fileContents):
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "world size":
                self._worldsize = (int(info[1]), int(info[2]))

    def draw(self, screen):
        self._background.draw(screen)
        for area in self._selectionAreas:
            area.draw(screen)
        for blob in self._blobs:
            blob.draw(screen)
        for letter in self._text:
            letter.draw(screen)

def main():
    parser = MenuParser("blobmenu.txt")
    parser.loadMenu()
    

if __name__ == "__main__":
   main()
