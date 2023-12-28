import pygame
import sys
from state import *


#TODO next: 
# - add shop and ability to buy things
# - add potions
# - make sure I can upgrade damage in shop
# - change the gun and rocket to 

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))

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