from world import *
from bullet import *


# make it so that the color eq works
class Player:
    def __init__(self):
        # self.pos = [WIDTH/2-tileSize/2,HEIGHT/2-tileSize/2]
        self.size = tileSize  #unit in pixels
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.visionRadius = 20 #units in blocks
        self.velocityX = 0
        self.velocityY = 0
        self.acceleration = .3
        self.maxVelocity = 5
        # self.rect = pygame.Rect(100, 100, self.size, self.size)
        self.rect = pygame.Rect(WIDTH/2-tileSize/2-60, HEIGHT/2-tileSize/2, self.size, self.size)
        pygame.draw.circle(self.surface, (255,255,255), (self.size/2, self.size/2), self.size/2)
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False 
        self.health = 10
        self.maxHealth = 10
        self.turretAngle = 0
        self.bullets = []
        self.bulletVelocity = 4
        Bullet.rangeOfVision = self.visionRadius + 4

    def render(self, surface):
        rad = tileSize/2-3
        pygame.draw.circle(self.surface, (255,255,255), (self.size/2, self.size/2), self.size/2)
        pygame.draw.circle(self.surface, (255,0,0), (rad*math.cos(self.turretAngle)+tileSize/2, rad*math.sin(self.turretAngle)+tileSize/2), 2)
        surface.blit(self.surface, (self.rect.x+camera.offset[0], self.rect.y+camera.offset[1]))
        for bullet in self.bullets:
            bullet.render(surface, self.rect.center)

    def playerGridPos(self):
        return (int(self.rect.center[0]/tileSize), int(self.rect.center[1]/tileSize))

    def update(self):
        willHitX, rectx = self.willHitBoxX(self.velocityX, self.rect)
        willHitY, recty = self.willHitBoxY(self.velocityY, self.rect)
        if not willHitX:
            self.rect.x += self.velocityX
        
        if not willHitY:
            self.rect.y += self.velocityY

        if self.movingLeft or self.movingRight:
            if self.movingLeft:
                if self.velocityX > -self.maxVelocity:
                    self.velocityX -= self.acceleration
            if self.movingRight:
                if self.velocityX < self.maxVelocity:
                    self.velocityX += self.acceleration
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
                    self.velocityY -= self.acceleration
            if self.movingDown:
                if self.velocityY < self.maxVelocity:
                    self.velocityY += self.acceleration
        else:
            if self.velocityY < 0:
                self.velocityY += self.acceleration
            if self.velocityY > 0:
                self.velocityY -= self.acceleration
            if self.velocityY < self.acceleration and self.velocityY > -self.acceleration:
                self.velocityY = 0

        for bullet in self.bullets:
            bullet.update()
            willHit, tile = bullet.willHitSomething(world.collisionRectMap)
            if willHit:
                self.bullets.remove(bullet)
                if type(tile) == Tile:
                    if tile.breakable:
                        world.collisionRectMap.remove(tile)
                if type(tile) == Torch:
                    if tile.lit == False:
                        tile.light()


        camera.lerpToPos(self.rect.center)
            
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
                    self.bullets.append(Bullet(self.rect.center, self.bulletVelocity, self.turretAngle))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.movingUp = False
                if event.key == pygame.K_DOWN:
                    self.movingDown = False 
                if event.key == pygame.K_LEFT:
                    self.movingLeft = False 
                if event.key == pygame.K_RIGHT:
                    self.movingRight = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.turretAngle += .2
        if keys[pygame.K_a]:
            self.turretAngle -= .2

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


player = Player()