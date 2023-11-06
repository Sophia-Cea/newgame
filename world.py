from utils import *
import json


class World:
    def __init__(self):
        f = open('map.json')
        data = json.load(f)
        f.close()
        self.map = data["backgroundMap"] #2d array
        self.collisionRectMap = [] #1d array
        self.tileSize = tileSize
        self.rangeOfVison = 10
        self.generateRectMap()

    def setRangeOfVison(self, val):
        self.rangeOfVison = val
    
    def generateRectMap(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 1:
                    self.collisionRectMap.append(pygame.Rect(j*self.tileSize, i*self.tileSize, self.tileSize, self.tileSize))

    def render(self, screen, playerPos):
        for rect in self.collisionRectMap:
            dist = calculateDistance((rect.center[0]/tileSize, rect.center[1]/tileSize), playerPos)
            # colorNum = clampColor(255*(self.rangeOfVison/dist-1)/9)
            colorNum = 255
            color = (colorNum, colorNum, colorNum)
            pygame.draw.rect(screen, color, rect)



    def update(self):
        pass

    def handleInput(self, events):
        pass


world = World()