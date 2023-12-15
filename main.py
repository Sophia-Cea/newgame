import pygame
import sys
from state import *

# TODO: 
# - make map bigger
# - add monsters~
# - health bar
# - money 
# - maybe theres stuff in the floor and you can dig up stuff???
# - caves!!! you have to dig to get from one cave to another
# - maybe some particle effects when the blocks explode
# - rockets or bombs or smth that increase the number of blocks that break when shooting
# - maybe some of the next levels can be traveled to by going down underground through a lil hole


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
    screen.blit(display, (0,0))
    pygame.display.flip()
    delta = fpsClock.tick(60)/1000