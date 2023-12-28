from utils import *

class Bullet:
    bulletSize = 4
    rangeOfVision = 0
    def __init__(self, pos, velocity, angle):
        self.rect = pygame.Rect(pos[0],pos[1], Bullet.bulletSize, Bullet.bulletSize)
        self.velocity = velocity
        self.angle = angle

    def render(self, screen, playerPos):
        dist = calculateDistance((self.rect.center[0]/tileSize, self.rect.center[1]/tileSize), (int(playerPos[0]/tileSize), int(playerPos[1]/tileSize)))
        colorNum = clampColor(255*(Bullet.rangeOfVision/(math.pow(dist, 2)+.1))/9)
        pygame.draw.circle(screen, (0,colorNum,0), (self.rect.x+camera.offset[0], self.rect.y+camera.offset[1]), 3)

    def update(self):
        self.rect.x += self.velocity * math.cos(self.angle) * delta
        self.rect.y += self.velocity * math.sin(self.angle) * delta

    def willHitSomething(self, worldMap):
        for tile in worldMap:
            if self.rect.colliderect(tile.rect):
                return True, tile
        return False, None

    def willHitEnemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True, enemy
        return False, None