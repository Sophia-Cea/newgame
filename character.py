from world import *
from bullet import *


# make it so that the color eq works
class Player:
    def __init__(self):
        # self.pos = [WIDTH/2-tileSize/2,HEIGHT/2-tileSize/2]
        self.size = tileSize  #unit in pixels
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.visionRadius = 50 #units in blocks
        World.rangeOfVision = self.visionRadius
        self.velocityX = 0
        self.velocityY = 0
        self.acceleration = .3
        self.maxVelocity = 5
        self.rect = pygame.Rect(44*tileSize, 30*tileSize, self.size, self.size)
        pygame.draw.circle(self.surface, (255,255,255), (self.size/2, self.size/2), self.size/2)
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False 
        self.health = 100
        self.maxHealth = 10
        self.turretAngle = 0
        self.bullets = []
        self.bulletVelocity = 6
        Bullet.rangeOfVision = self.visionRadius + 4
        self.inventory = []
        self.money = 100
        self.animation = []
        self.animationDuration = 80
        self.animationCounter = 0
        self.currentFrame = 0
        self.createAnimation()
        self.currentTool = 0 #0: gun, 1: shovel, 2: pickaxe
        self.bulletDamage = 3

    def createAnimation(self):
        scale = 4
        for i in range(13):
            self.animation.append(pygame.image.load("assets/player/player" + str(i+1) + ".png"))
            self.animation[i] = pygame.transform.scale(self.animation[i], (self.rect.width*1.2, self.rect.width*8/7*1.2))

    def render(self, surface):
        rad = tileSize/2-3
        # pygame.draw.circle(self.surface, (255,255,255), (self.size/2, self.size/2), self.size/2)
        # pygame.draw.circle(self.surface, (255,0,0), (rad*math.cos(self.turretAngle)+tileSize/2, rad*math.sin(self.turretAngle)+tileSize/2), 2)
        # surface.blit(self.surface, (self.rect.x+camera.offset[0], self.rect.y+camera.offset[1]))
        surface.blit(self.animation[self.currentFrame], (self.rect.x+camera.offset[0], self.rect.y+camera.offset[1]-(self.animation[0].get_height()-self.rect.height)))
        for bullet in self.bullets:
            bullet.render(surface, self.rect.center)

    def playerGridPos(self):
        return (int(self.rect.center[0]/tileSize), int(self.rect.center[1]/tileSize))

    def update(self):
        # animation control
        if self.animationCounter < self.animationDuration:
            self.animationCounter += 1
        else: 
            self.animationCounter = 0
        self.currentFrame = int(self.animationCounter/(self.animationDuration/len(self.animation))) #fix this
        if self.currentFrame > len(self.animation)-1:
            self.currentFrame = 0
        
        # collision control
        willHitX, rectx = self.willHitBoxX(self.velocityX)
        willHitY, recty = self.willHitBoxY(self.velocityY)
        if rectx != None:
            rectx = rectx.rect
        if recty != None:
            recty = recty.rect
        if not willHitX:
            self.rect.x += self.velocityX
        if not willHitY:
            self.rect.y += self.velocityY

        # movement control
        if self.movingLeft or self.movingRight:
            if self.movingLeft:
                if self.velocityX > -self.maxVelocity:
                    self.velocityX -= self.acceleration * delta
            if self.movingRight:
                if self.velocityX < self.maxVelocity:
                    self.velocityX += self.acceleration * delta
        else:
            if self.velocityX < 0:
                self.velocityX += self.acceleration
            if self.velocityX > 0:
                self.velocityX -= self.acceleration
            if self.velocityX < self.acceleration and self.velocityX > -self.acceleration:
                self.velocityX = 0

        if self.movingUp or self.movingDown:
            if self.movingUp:
                if self.velocityY > -self.maxVelocity:
                    self.velocityY -= self.acceleration * delta
            if self.movingDown:
                if self.velocityY < self.maxVelocity:
                    self.velocityY += self.acceleration * delta
        else:
            if self.velocityY < 0:
                self.velocityY += self.acceleration
            if self.velocityY > 0:
                self.velocityY -= self.acceleration
            if self.velocityY < self.acceleration and self.velocityY > -self.acceleration:
                self.velocityY = 0

        # turret direction control
        if self.movingDown and self.movingLeft:
            self.turretAngle = 3*math.pi/4
        elif self.movingDown and self.movingRight:
            self.turretAngle = math.pi/4
        elif self.movingUp and self.movingLeft:
            self.turretAngle = 5*math.pi/4
        elif self.movingUp and self.movingRight:
            self.turretAngle = 7*math.pi/4
        elif self.movingLeft and not self.movingDown or self.movingLeft and not self.movingUp:
            self.turretAngle = math.pi
        elif self.movingRight and not self.movingDown or self.movingRight and not self.movingUp:
            self.turretAngle = 0
        elif self.movingUp and not self.movingLeft or self.movingUp and not self.movingRight:
            self.turretAngle = math.pi * 3/2
        elif self.movingDown and not self.movingLeft or self.movingDown and not self.movingRight:
            self.turretAngle = math.pi/2

        # bullet control
        for bullet in self.bullets:
            bullet.update()
            willHit, tile = bullet.willHitSomething(world.collisionRectMap)
            willHitEnemy, enemy = bullet.willHitEnemy(Level1.enemies)
            if willHit:
                self.bullets.remove(bullet)
                if type(tile) == Torch:
                    if tile.lit == False:
                        tile.light()
            if willHitEnemy:
                self.bullets.remove(bullet)
                enemy.health -= self.bulletDamage

        # camera control
        camera.lerpToPos(self.rect.center)

    def checkLootDrop(self):
        chance = randint(1,10)
        if chance == 5:
            self.money += randint(1,8)


    def handleInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.movingUp = True
                if event.key == pygame.K_DOWN:
                    self.movingDown = True 
                if event.key == pygame.K_LEFT:
                    self.movingLeft = True 
                if event.key == pygame.K_RIGHT:
                    self.movingRight = True
                
                if event.key == pygame.K_SPACE:
                    if self.currentTool == 0:
                        self.bullets.append(Bullet(self.rect.center, self.bulletVelocity, self.turretAngle))
                    
                    elif self.currentTool == 1: # shovel
                        for tile in world.groundRectMap:
                            if tile.rect.collidepoint(self.rect.center):
                                world.groundRectMap.remove(tile)
                                if tile.hasValue:
                                    self.money += randint(1,8)

                    elif self.currentTool == 2: #pickaxe
                        willHitLeft, tileLeft = self.willHitBoxX(-5)
                        willHitRight, tileRight = self.willHitBoxX(5)
                        willHitUp, tileUp = self.willHitBoxY(-5)
                        willHitDown, tileDown = self.willHitBoxY(5)
                        if self.movingLeft and willHitLeft and type(tileLeft) == Tile and tileLeft.breakable:
                            world.collisionRectMap.remove(tileLeft)
                        elif self.movingRight and willHitRight and type(tileRight) == Tile and tileRight.breakable:
                            world.collisionRectMap.remove(tileRight)
                        elif self.movingUp and willHitUp and type(tileUp) == Tile and tileUp.breakable:
                            world.collisionRectMap.remove(tileUp)
                        elif self.movingDown and willHitDown and type(tileDown) == Tile and tileDown.breakable:
                            world.collisionRectMap.remove(tileDown)
                    
                
                if event.key == pygame.K_1:
                    self.currentTool = 0
                if event.key == pygame.K_2:
                    self.currentTool = 1
                if event.key == pygame.K_3:
                    self.currentTool = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.movingUp = False
                if event.key == pygame.K_DOWN:
                    self.movingDown = False 
                if event.key == pygame.K_LEFT:
                    self.movingLeft = False 
                if event.key == pygame.K_RIGHT:
                    self.movingRight = False


    def willHitBoxX(self, distance):
        for tile in world.collisionRectMap:
            if (pygame.Rect(self.rect.x+distance, self.rect.y, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile
        return False, None
    
    def willHitBoxY(self, distance):
        for tile in world.collisionRectMap:
            if (pygame.Rect(self.rect.x, self.rect.y+distance, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile
        return False, None
    
    def willHitBoxXGround(self, distance):
        for tile in world.groundMap:
            if (pygame.Rect(self.rect.x+distance, self.rect.y, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile
        return False, None
    
    def willHitBoxYGround(self, distance):
        for tile in world.groundRectMap:
            if (pygame.Rect(self.rect.x, self.rect.y+distance, self.rect.width, self.rect.height).colliderect(tile.rect)):
                return True, tile
        return False, None



class InventoryItem:
    items = []
    mushrooms = {"g"}
    def __init__(self) -> None:
        pass

class DoorKey(InventoryItem):
    def __init__(self, door) -> None:
        super().__init__()
        self.doorToUnlock = door

class Potion:
    def __init__(self) -> None:
        pass



player = Player()