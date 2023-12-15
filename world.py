from utils import *
import json




class Tile:
    def __init__(self, tileType, pos):
        self.tileType = tileType
        self.rect = pygame.Rect(pos[0]*tileSize, pos[1]*tileSize, tileSize, tileSize)
        self.breakable = False
        if self.tileType == 3:
            self.breakable = True
    
    def render(self, screen, distVal):
        color1 = (clampColor(255*distVal), clampColor(255*distVal), clampColor(255*distVal))
        # color2 = (clampColor(90*distVal), clampColor(90*distVal), clampColor(255*distVal))
        color3 = (clampColor(180*distVal), clampColor(180*distVal), clampColor(180*distVal))
        if self.tileType == 1:
            pygame.draw.rect(screen, color1, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))
        if self.tileType == 2:
            if distVal < .1:
                distVal = .1
            color2 = (clampColor(90*distVal), clampColor(90*distVal), clampColor(255*distVal))
            pygame.draw.rect(screen, color2, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))
        if self.tileType == 3:
            pygame.draw.rect(screen, color3, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))

    def calculateTorchDistance(self):
        torchDist = 0
        for torch in Torch.torches:
            if torch.lit:
                dist = calculateDistance((self.rect.center[0]/tileSize, self.rect.center[1]/tileSize), (torch.rect.center[0]/tileSize, torch.rect.center[1]/tileSize))
                newDist = (World.rangeOfVision/math.pow(dist, 1.7))/9
                if newDist > torchDist:
                    torchDist = newDist
        return torchDist

class Torch:
    color = (255,210,50)
    unlitColor = (170,140,40)
    torches = []
    def __init__(self, pos, lightRadius):
        self.lightRadius = lightRadius
        self.rect = pygame.Rect(pos[0]*tileSize, pos[1]*tileSize, tileSize, tileSize)
        self.lit = False
        Torch.torches.append(self)

    def render(self, screen, distValue=1):
        if self.lit:
            pygame.draw.rect(screen, Torch.color, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))
        else:
            color = (clampColor(Torch.unlitColor[0]*distValue), clampColor(Torch.unlitColor[1]*distValue), clampColor(Torch.unlitColor[2]*distValue))
            pygame.draw.rect(screen, color, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))
    
    def light(self):
        self.lit = True


class World:
    rangeOfVision = 10
    def __init__(self):
        f = open('map.json')
        data = json.load(f)
        f.close()
        self.map = data["backgroundMap"] #2d array
        self.collisionRectMap = [] #1d array
        self.tileSize = tileSize
        self.generateRectMap()

    def setRangeOfVision(self, val):
        World.rangeOfVision = val
    
    def generateRectMap(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                    if self.map[i][j] != 0:
                        if self.map[i][j] == 4:
                            self.collisionRectMap.append(Torch((j,i), World.rangeOfVision))
                        else:
                            self.collisionRectMap.append(Tile(self.map[i][j], (j,i)))


    def render(self, screen, playerPos):
        for tile in self.collisionRectMap:
            dist = calculateDistance((tile.rect.center[0]/tileSize, tile.rect.center[1]/tileSize), playerPos)
            distValue = (World.rangeOfVision/math.pow(dist, 2))/9
            if distValue > 1:
                distValue = 1
            if self.isOnscreen(tile.rect):
                if type(tile) == Tile:
                    torchDist = tile.calculateTorchDistance()
                    if torchDist > distValue:
                        distValue = torchDist
                    tile.render(screen, distValue)
                elif type(tile) == Torch:
                    tile.render(screen, distValue)


    def isOnscreen(self, rect):
        if rect.x + camera.offset[0] + tileSize < 0:
            return False
        if rect.x + camera.offset[0] > WIDTH:
            return False
        if rect.y + camera.offset[1] + tileSize < 0:
            return False
        if rect.y + camera.offset[1] > HEIGHT:
            return False
        return True


    def update(self):
        pass

    def handleInput(self, events):
        pass


world = World()



