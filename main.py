import pygame
import sys
# from utils import *
from state import *

# TODO: 
# - fix collitions
# - fix camera so that tiles off screen don't render
# - make map bigger
# - add bullets~

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))
stateManager = StateManager()

stateManager.push(PlayState())

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    WIDTH, HEIGHT = screen.get_size()
    stateManager.run(display, events)
    pygame.transform.scale(display, (WIDTH, HEIGHT))
    screen.fill((255,255,255))
    # screen.fill((0,0,0))
    screen.blit(display, camera.offset)
    # pygame.draw.circle(screen, (255,0,0), (WIDTH/2, HEIGHT/2), 5)
    pygame.display.flip()
    delta = fpsClock.tick(60)/1000