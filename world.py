from utils import *
import json
global world




class Tile:
    def __init__(self, tileType, pos):
        self.tileType = tileType
        self.rect = pygame.Rect(pos[0]*tileSize, pos[1]*tileSize, tileSize, tileSize)
        self.breakable = False
        self.isWater = False
        if self.tileType == 3:
            self.breakable = True
        if self.tileType == 1: # wall
            self.color = (255,255,255)
        elif self.tileType == 2: # water
            self.color = (90,90,255)
        elif self.tileType == 3: # breakable tile
            self.color = (160,160,200)
        elif self.tileType == 5: # locked door
            self.color = (180,0,220)
        else:
            self.color = (255,0,0)
    
    def render(self, screen, distVal):
        if self.isWater:
            if distVal < .1:
                distVal = .1
        color = (clampColor(self.color[0]*distVal), clampColor(self.color[1]*distVal), clampColor(self.color[2]*distVal))
        pygame.draw.rect(screen, color, pygame.Rect(self.rect.x+camera.offset[0], self.rect.y+camera.offset[1], self.rect.width, self.rect.height))

    def calculateTorchDistance(self):
        torchDist = 0
        for torch in Torch.torches:
            if torch.lit:
                dist = calculateDistance((self.rect.center[0]/tileSize, self.rect.center[1]/tileSize), (torch.rect.center[0]/tileSize, torch.rect.center[1]/tileSize))
                newDist = (World.rangeOfVision/(math.pow(dist, 1.7)+.00001))/9
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

class DiggableTile(Tile):
    def __init__(self, tileType, pos):
        super().__init__(tileType, pos)
        self.hasValue = False
        self.givesCrystal = True

        if self.tileType == 1:
            self.color = (200,150,150)
        elif self.tileType == 2:
            self.color = (150,200,150)
            self.hasValue = True
            self.givesCrystal = True
        elif self.tileType == 3:
            self.color = (150,150,200)
        elif self.tileType == 4:
            self.color = (200,150,200)
        else:
            self.color = (0,0,255)

class World:
    rangeOfVision = 10
    def __init__(self):
        self.collisionRectMap = [] #1d array
        self.groundRectMap = [] #1d array
        self.tileSize = tileSize
        self.generateRectMap()
        self.fuel = 0
        self.requiredFuel = 100
        self.playerStartPos = [0,0]
    
    def addFuel(self, amount):
        if self.fuel < self.requiredFuel:
            self.fuel += amount
        if self.fuel > self.requiredFuel:
            self.fuel = self.requiredFuel

    def setRangeOfVision(self, val):
        World.rangeOfVision = val

    def generateGroundMap(self):
        for i in range(len(self.map)):
            temp = []
            for j in range(len(self.map[0])):
                num = randint(0,4)
                temp.append(num)
            self.groundMap.append(temp)


    def createMap(self, levelNum):
        f = open('level' + str(levelNum) + '.json')
        data = json.load(f)
        f.close()
        self.map = data["obstacleMap"] #2d array
        self.groundMap = [] #2d array of ints
        self.generateGroundMap()
    
    def generateRectMap(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                    if self.map[i][j] != 0:
                        if self.map[i][j] == 4:
                            self.collisionRectMap.append(Torch((j,i), World.rangeOfVision))
                        else:
                            self.collisionRectMap.append(Tile(self.map[i][j], (j,i)))
                            if self.map[i][j] == 2:
                                self.collisionRectMap[-1].isWater = True
                    if self.groundMap[i][j] != 0:
                        self.groundRectMap.append(DiggableTile(self.groundMap[i][j], (j,i)))


    def render(self, screen, playerPos):
        for tile in self.groundRectMap:
            dist = calculateDistance((tile.rect.center[0]/tileSize, tile.rect.center[1]/tileSize), playerPos)
            distValue = (World.rangeOfVision/math.pow(dist, 2))/9
            if distValue > 1:
                distValue = 1
            if self.isOnscreen(tile.rect):
                torchDist = tile.calculateTorchDistance()
                if torchDist > distValue:
                    distValue = torchDist
                tile.render(screen, distValue)

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


class Level1(World):
    enemies = []
    def __init__(self, levelNum):
        self.levelNum = levelNum
        self.createMap(levelNum)
        super().__init__()
        self.requiredFuel = 100
        self.playerStartPos = [44,30]
    
    def update(self):
        super().update()
        if self.fuel >= self.requiredFuel:
            for tile in self.collisionRectMap:
                if type(tile) != Torch and tile.tileType == 5:
                    tile.breakable = True
    
    def checkPlayerWon(self, player):
        if player.rect.y > len(self.map) * tileSize:
            return True
        return False
    

class Level2(World):
    enemies = []
    def __init__(self, levelNum):
        self.levelNum = levelNum
        self.createMap(levelNum)
        super().__init__()
        self.requiredFuel = 100
        self.playerStartPos = [79,9]
    
    def update(self):
        super().update()
        if self.fuel >= self.requiredFuel:
            for tile in self.collisionRectMap:
                if type(tile) != Torch and tile.tileType == 5:
                    tile.breakable = True
    
    def checkPlayerWon(self, player):
        if player.rect.y > len(self.map) * tileSize:
            return True
        return False


world = Level1(1)



