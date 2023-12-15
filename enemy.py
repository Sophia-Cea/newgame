from character import *


class Enemy:
    def __init__(self):
        self.pos = self.pickRandomPos() # in tiles
        self.rect = pygame.Rect(self.pos[0]*tileSize, self.pos[1]*tileSize, tileSize, tileSize)
        self.velocity = 4 # in pixels
        self.visionRange = 5 # in tiles
        # self.targetPos = self.pickRandomPos()
        self.getPath()
        self.targetPos = self.path[0]
        self.deviatedFromPath = False

    def render(self, screen):
        dist = calculateDistance((self.rect.center[0]/tileSize, self.rect.center[1]/tileSize), (int(player.rect.center[0]/tileSize), int(player.rect.center[1]/tileSize)))
        colorNum = clampColor(255*(player.visionRadius/math.pow(dist-1, 2))/9)
        pygame.draw.circle(screen, (colorNum,0,0), (self.rect.x+camera.offset[0]-tileSize/2, self.rect.y+camera.offset[1]-tileSize/2), tileSize/2)

    def update(self):
        if self.canSeePlayer():
            # im sure this will cause some errors at some point
            self.path = astar((int(self.rect.x/tileSize), int(self.rect.y/tileSize)), (int(player.rect.x/tileSize), int(player.rect.y/tileSize)), world.map)[1:]
            if self.path != None and len(self.path) > 1:
                self.targetPos = self.path[0]
            self.deviatedFromPath = True
        else:
            if not self.deviatedFromPath:
                self.rect.x += ((self.targetPos[0] - int(self.rect.x/tileSize)) * 2)
                self.rect.y += ((self.targetPos[1] - int(self.rect.y/tileSize)) * 2)

            if self.deviatedFromPath:
                self.getPath()
                self.targetPos = self.path[0]
                self.deviatedFromPath = False

        self.rect.x += ((self.targetPos[0] - int(self.rect.x/tileSize)) * 4)
        self.rect.y += ((self.targetPos[1] - int(self.rect.y/tileSize)) * 4)


        if self.rect.colliderect(pygame.Rect(self.targetPos[0]*tileSize,self.targetPos[1]*tileSize, tileSize, tileSize)):
            if len(self.path) > 1:
                self.path = self.path[1:]
            else:
                self.getPath()
            self.targetPos = self.path[0]

    def handleInput(self, events):
        pass

    def canSeePlayer(self):
        if calculateDistance(self.rect.center, player.rect.center) < tileSize*self.visionRange:
            return True
        return False
    
    def pickRandomPos(self):
        xpos = randint(0,len(world.map[0])-1)
        ypos = randint(0,len(world.map)-1)
        for rect in world.collisionRectMap:
            if int(rect.x/tileSize) == xpos and int(rect.y/tileSize) == ypos:
                self.pickRandomPos()
        return (xpos, ypos)

    def getPath(self):
        self.path = astar((int(self.rect.x/tileSize), int(self.rect.y/tileSize)), self.pickRandomPos(), world.map)
        if self.path == None or len(self.path) < 3:
            self.getPath()
        self.path = self.path[1:]