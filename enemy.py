from character import *


class Enemy:
    visionRange = 5 #in tiles
    def __init__(self, startPos):
        self.startPos = startPos
        self.rect = pygame.Rect(self.startPos[0]*tileSize, self.startPos[1]*tileSize, tileSize, tileSize)
        self.velocity = 1 # in pixels
        self.color = (255,0,0)
        self.health = 20

    def render(self, screen):
        dist = calculateDistance(self.rect.center, player.rect.center)
        torchDist = 100
        for torch in world.collisionRectMap:
            if type(torch) == Torch and torch.lit:
                newDist = calculateDistance(self.rect.center, torch.rect.center)
                if newDist < torchDist:
                    torchDist = newDist

        if torchDist < dist:
            dist = torchDist
        color = (clampColor(self.color[0]*(player.visionRadius*tileSize/(abs(math.pow(dist, 1.3))+.001))/5), clampColor(self.color[1]*(player.visionRadius*tileSize/(abs(math.pow(dist, 1.3))+.001))/5), clampColor(self.color[2]*(player.visionRadius*tileSize/(abs(math.pow(dist, 1.3))+.001))/5))
        pygame.draw.circle(screen, color, (self.rect.center[0]+camera.offset[0], self.rect.center[1]+camera.offset[1]), tileSize/2)
        

    def update(self):
        pass

    def handleInput(self, events):
        pass

    def canSeePlayer(self):
        if calculateDistance(self.rect.center, player.rect.center) < tileSize*self.visionRange:
            return True
        return False


class Patroller(Enemy):
    def __init__(self, startPos, direction, distance):
        self.direction = direction #1,2,3,4 : up, right, down, left
        self.distance = distance * tileSize
        self.startPos = startPos
        self.walkingBack = False
        self.distanceTraveled = 0
        if self.direction == 1:
            self.endPos = (self.startPos[0], self.startPos[1]-self.distance)
        elif self.direction == 2:
            self.endPos = (self.startPos[0]+self.distance, self.startPos[1])
        elif self.direction == 3:
            self.endPos = (self.startPos[0], self.startPos[1]+self.distance)
        elif self.direction == 4:
            self.endPos = (self.startPos[0]-self.distance, self.startPos[1])
        super().__init__(self.startPos)
        self.endPosPixels = (self.endPos[0]*tileSize, self.endPos[1]*tileSize)
        self.startPosPixels = (self.rect.center[0]*tileSize, self.rect.center[1]*tileSize)
        self.bullets = []
        self.bulletFrequency = 100
        self.bulletDelay = 0
        self.bulletVelocity = 4
        self.damage = 2

    def render(self, screen):
        super().render(screen)
        for bullet in self.bullets:
            bullet.render(screen, player.rect.center)
    

    def update(self):
        if not self.canSeePlayer():
            if self.direction == 1: # verify it all works
                if self.walkingBack == False and self.distanceTraveled >= self.distance:
                    self.walkingBack = True
                    self.distanceTraveled = 0
                if self.walkingBack == False:
                    self.rect.y -= self.velocity * delta
                    self.distanceTraveled += self.velocity * delta
                if self.walkingBack and self.distanceTraveled >= self.distance:
                    self.walkingBack = False
                    self.distanceTraveled = 0
                if self.walkingBack:
                    self.rect.y += self.velocity * delta
                    self.distanceTraveled += self.velocity * delta

            elif self.direction == 3:
                if self.walkingBack == False and self.distanceTraveled >= self.distance:
                    self.walkingBack = True
                    self.distanceTraveled = 0
                if self.walkingBack == False:
                    self.rect.y += self.velocity * delta
                    self.distanceTraveled += self.velocity * delta
                if self.walkingBack and self.distanceTraveled >= self.distance:
                    self.walkingBack = False
                    self.distanceTraveled = 0
                if self.walkingBack:
                    self.rect.y -= self.velocity * delta
                    self.distanceTraveled += self.velocity * delta

            elif self.direction == 2:
                if self.walkingBack == False and self.distanceTraveled >= self.distance:
                    self.walkingBack = True
                    self.distanceTraveled = 0
                if self.walkingBack == False:
                    self.rect.x += self.velocity * delta
                    self.distanceTraveled += self.velocity * delta
                if self.walkingBack and self.distanceTraveled >= self.distance:
                    self.walkingBack = False
                    self.distanceTraveled = 0
                if self.walkingBack:
                    self.rect.x -= self.velocity * delta
                    self.distanceTraveled += self.velocity * delta

            elif self.direction == 4:
                if self.walkingBack == False and self.distanceTraveled >= self.distance:
                    self.walkingBack = True
                    self.distanceTraveled = 0
                if self.walkingBack == False:
                    self.rect.x -= self.velocity * delta
                    self.distanceTraveled += self.velocity * delta
                if self.walkingBack and self.distanceTraveled >= self.distance:
                    self.walkingBack = False
                    self.distanceTraveled = 0
                if self.walkingBack:
                    self.rect.x += self.velocity * delta
                    self.distanceTraveled += self.velocity * delta

        else:
            if self.bulletDelay == 0:
                bulletAngle = math.atan2((player.rect.centery-self.rect.centery),(player.rect.centerx-self.rect.centerx))
                self.bullets.append(Bullet(self.rect.center, self.bulletVelocity, bulletAngle))
            self.bulletDelay += 1
            if self.bulletDelay >= self.bulletFrequency:
                self.bulletDelay = 0

        for bullet in self.bullets:
            bullet.update()
            willHit, tile = bullet.willHitSomething(world.collisionRectMap)
            if bullet.rect.colliderect(player.rect):
                willHit = True
                player.health -= self.damage
            if willHit:
                self.bullets.remove(bullet)
 
class Explorer(Enemy):
    def __init__(self, startPos):
        super().__init__(startPos)
        self.direction = randint(1,4) #1, 2, 3, 4, up, right, down, left
        self.velocity = 2
        self.color = (0, 0, 255)
    
    def update(self):
        super().update()
        if self.direction == 1:
            willHitY, tile = self.willHitBoxY(-self.velocity)
            if not willHitY:
                self.rect.y -= self.velocity * delta
            else:
                self.pickNewDirection()
        elif self.direction == 3:
            willHitY, tile = self.willHitBoxY(self.velocity)
            if not willHitY:
                self.rect.y += self.velocity * delta
            else:
                self.pickNewDirection()
        elif self.direction == 2:
            willHitX, tile = self.willHitBoxX(self.velocity)
            if not willHitX:
                self.rect.x += self.velocity * delta
            else:
                self.pickNewDirection()
        elif self.direction == 4:
            willHitX, tile = self.willHitBoxX(-self.velocity)
            if not willHitX:
                self.rect.x -= self.velocity * delta
            else:
                self.pickNewDirection()

    def pickNewDirection(self):
        self.direction = randint(1,4)
        if self.direction == 1:
            willHitY, tiley = self.willHitBoxY(-self.velocity)
            if willHitY:
                self.pickNewDirection()
        elif self.direction == 3:
            willHitY, tiley = self.willHitBoxY(self.velocity)
            if willHitY:
                self.pickNewDirection()
        elif self.direction == 2:
            willHitX, tilex = self.willHitBoxX(self.velocity)
            if willHitX:
                self.pickNewDirection()
        elif self.direction == 4:
            willHitX, tilex = self.willHitBoxX(-self.velocity)
            if willHitX:
                self.pickNewDirection()
    
    def checkCanMove(self):
        pass #check if it can even go anywhere to avoid infinite looping

    
    def willHitBoxX(self, distance):
        for tile in world.collisionRectMap:
            if (pygame.Rect(self.rect.x+distance, self.rect.y, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile.rect
        return False, None
    
    def willHitBoxY(self, distance):
        for tile in world.collisionRectMap:
            if (pygame.Rect(self.rect.x, self.rect.y+distance, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile.rect
        return False, None






















class Explorer2(Enemy):
    def __init__(self):
        super().__init__()
        self.pos = self.pickRandomPos() # in tiles
        self.rect = pygame.Rect(self.pos[0]*tileSize, self.pos[1]*tileSize, tileSize, tileSize)
        self.velocity = 2 # in pixels
        self.visionRange = 5 # in tiles
        # self.targetPos = self.pickRandomPos()
        self.getPath()
        self.targetPos = self.path[0]
        self.deviatedFromPath = False

    def willHitBoxX(self, distance, rectObj):
        for tile in world.collisionRectMap:
            if (pygame.Rect(rectObj.x+distance, rectObj.y, rectObj.width, rectObj.height).colliderect(tile.rect)):
                return True, tile.rect
        return False, None
    
    def willHitBoxY(self, distance, rectObj):
        for tile in world.collisionRectMap:
            if (pygame.Rect(rectObj.x, rectObj.y+distance, rectObj.width, rectObj.height).colliderect(tile.rect)):
                return True, tile.rect
        return False, None

    def update(self):
        if self.canSeePlayer():
            # self.targetPos = player.playerGridPos()
            dist = calculateDistance(self.rect.center, player.rect.center)
            if dist == 0:
                dist = .1
            unitVec = ((player.rect.x-self.rect.x)/dist, (player.rect.y-self.rect.y)/dist)
            velocityVec = (unitVec[0]*self.velocity, unitVec[1]*self.velocity)
            if not self.willHitBoxX(velocityVec[0], self.rect):
                self.rect.x += velocityVec[0]
            if not self.willHitBoxY(velocityVec[1], self.rect):
                self.rect.y += velocityVec[1]
            self.deviatedFromPath = True
            # # im sure this will cause some errors at some point
            # self.path = astar((int(self.rect.x/tileSize), int(self.rect.y/tileSize)), (int(player.rect.x/tileSize), int(player.rect.y/tileSize)), world.map)[1:]
            # if self.path != None and len(self.path) > 1:
            #     self.targetPos = self.path[0]
            # self.deviatedFromPath = True
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
        for tile in world.collisionRectMap:
            if int(tile.rect.x/tileSize) == xpos and int(tile.rect.y/tileSize) == ypos:
                self.pickRandomPos()
        return (xpos, ypos)

    def getPath(self):
        randomPos = self.pickRandomPos()
        self.path = astar((int(self.rect.x/tileSize), int(self.rect.y/tileSize)), randomPos, world.map)
        try:
            if self.path == None or len(self.path) < 3:
                self.getPath()
            self.path = self.path[1:]
        except:
            print("error getting a path")
            print(randomPos)
            if self.path == None or len(self.path) < 3:
                self.getPath()
            self.path = self.path[1:]