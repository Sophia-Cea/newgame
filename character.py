from world import *


# make it so that the color eq works
class Player:
    def __init__(self):
        # self.pos = [WIDTH/2-tileSize/2,HEIGHT/2-tileSize/2]
        self.size = tileSize  #unit in pixels
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.visionRadius = 10 #units in blocks
        self.velocityX = 0
        self.velocityY = 0
        self.acceleration = .3
        self.maxVelocity = 5
        self.rect = pygame.Rect(WIDTH/2-tileSize/2, HEIGHT/2-tileSize/2, self.size, self.size)
        pygame.draw.circle(self.surface, (255,255,255), (self.size/2, self.size/2), self.size/2)

    def render(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))

    def playerGridPos(self):
        return (int(self.rect.center[0]/tileSize), int(self.rect.center[1]/tileSize))

    def update(self):

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
        if self.velocityX != 0:
            if self.velocityX < 0:
                self.velocityX += self.acceleration
            else:
                self.velocityX -= self.acceleration
            if self.velocityX > -self.acceleration and self.velocityX < self.acceleration:
                self.velocityX = 0
        if self.velocityY != 0:
            if self.velocityY < 0:
                self.velocityY += self.acceleration
            else:
                self.velocityY -= self.acceleration
            if self.velocityY > -self.acceleration and self.velocityY < self.acceleration:
                self.velocityY = 0
        camera.lerpToPos(self.rect.center)
        print(self.playerGridPos())
            

    
    def handleInput(self, events):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            willHit, rectHit = self.willHitBoxY(-self.velocityY-self.acceleration)
            if not willHit:
                if abs(self.velocityY) < self.maxVelocity:
                    self.velocityY -= self.acceleration*2
            else:
                self.rect.top = rectHit.bottom + self.acceleration * 2
                self.velocityY = 0

        if keys[pygame.K_DOWN]:
            willHit, rectHit = self.willHitBoxY(self.velocityY+self.acceleration)
            if not willHit:
                if abs(self.velocityY) < self.maxVelocity:
                    self.velocityY += self.acceleration*2
            else:
                self.rect.bottom = rectHit.top - self.acceleration*2
                self.velocityY = 0

        if keys[pygame.K_LEFT]:
            willHit, rectHit = self.willHitBoxX(-self.velocityX-self.acceleration)
            if not willHit:
                if abs(self.velocityX) < self.maxVelocity:
                    self.velocityX -= self.acceleration*2
            else:
                self.rect.left = rectHit.right - self.acceleration * 2
                self.velocityX = 0

        if keys[pygame.K_RIGHT]:
            willHit, rectHit = self.willHitBoxX(self.velocityX+self.acceleration)
            if not willHit:
                if abs(self.velocityX) < self.maxVelocity:
                    self.velocityX += self.acceleration*2
            else:
                self.rect.right = rectHit.left + self.acceleration * 2
                self.velocityY = 0

    def willHitBoxX(self, distance):
        for rect in world.collisionRectMap:
            if (pygame.Rect(self.rect.x+distance, self.rect.y, self.rect.width, self.rect.height).colliderect(rect)):
                return True, rect
        return False, None
    
    def willHitBoxY(self, distance):
        for rect in world.collisionRectMap:
            if (pygame.Rect(self.rect.x, self.rect.y+distance, self.rect.width, self.rect.height).colliderect(rect)):
                return True, rect
        return False, None
