import pygame
import sys
from state import *


#TODO next: 
# - change the gun and rocket to wand and fireballs n shit



# BUG:
# - redo lighting
# - fix the fucked up collisions

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))



def setIcon():
    icon = pygame.image.load("assets/player/player1.png")
    icon = pygame.transform.scale(icon, (icon.get_width()*4,icon.get_height()*4))
    iconSurf = pygame.Surface((icon.get_width(), icon.get_height()+7),pygame.SRCALPHA)
    iconSurf.blit(icon, (0,0))
    pygame.display.set_icon(iconSurf)

setIcon()

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