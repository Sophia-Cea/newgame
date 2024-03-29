import pygame
import sys
import os
import math
from random import *
import heapq

pygame.init()
WIDTH = 1000
HEIGHT = 700
delta = 1
tileSize = 40

class Camera:
    def __init__(self):
        self.offset = [-1300, -900]
        # self.offset = [0, 0]
        self.targetPos = [0,0]
        self.lerpconst = .1

    def updateOffset(self, x, y):
        self.offset = [self.offset[0]-x, self.offset[1]-y]
    
    def lerpToPos(self, pos):
        self.targetPos = [-(pos[0]-WIDTH/2), -(pos[1]-HEIGHT/2)]

    def update(self):
        if self.offset != self.targetPos:
            self.offset[0] += (self.targetPos[0] - self.offset[0]) * self.lerpconst * delta
            self.offset[1] += (self.targetPos[1] - self.offset[1]) * self.lerpconst * delta


camera = Camera()

def gradient(col1, col2, surface, rect=None):
    if rect == None:
        rect = pygame.Rect(0,0, surface.get_width(), surface.get_height())

    if type(col1) != tuple:
        col1 = col1.copy()
    if type(col2) != tuple:
        col2 = col2.copy()
    inc1 = (col2[0] - col1[0])/rect.height
    inc2 = (col2[1] - col1[1])/rect.height
    inc3 = (col2[2] - col1[2])/rect.height
    color = [col1[0], col1[1], col1[2]]
    for i in range(rect.height):
        pygame.draw.line(surface, color, (rect.x, rect.y + i), (rect.width, rect.y + i), 2)
        color[0] += inc1
        color[1] += inc2
        color[2] += inc3

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

def calculateDistance(point1, point2):
    return math.sqrt(math.pow(point1[0]-point2[0], 2) + math.pow(point1[1]-point2[1], 2))

def clampColor(val):
    if val > 255:
        val = 255
    if val < 0:
        val = 0
    return int(val)

def convertRect(rectTuple):
    newRect = rectTuple
    return pygame.Rect(WIDTH/100*newRect[0], HEIGHT/100*newRect[1], WIDTH/100*newRect[2], HEIGHT/100*newRect[3])

class Colors:
    col1 = [248, 248, 255]
    col2 = [237, 87, 82]
    col3 = [51, 51, 51]
    col4 = [214, 233, 252]
    col5 = [146, 170, 199]

    textCol = col3.copy()
    bgCol1 = col1.copy()
    bgCol2 = col1.copy()
    buttonCol1 = col4.copy()
    buttonCol2 = col5.copy()
    accentCol = col2.copy()

class Fonts:
    WIDTH = WIDTH
    HEIGHT = HEIGHT
    fonts = {
        "title": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/18)),
        "subtitle": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/24)),
        "paragraph": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/30)),
        "button": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/28)),
        "button2": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/40)),
        "shopText": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/55)),
        "shopText2": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/70))
    }

    def resizeFonts(screen):
        Fonts.WIDTH = screen.get_width()
        Fonts.fonts = {
            "title": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/14)),
            "subtitle": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/20)),
            "paragraph": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/26)),
            "button": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/28)),
            "button2": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/35)),
            "shopText": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/67)),
        "shopText2": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/80))

        }

class Text:
    texts = []
    def __init__(self, text, font, color, position, centered, underline = False) -> None:
        self.content = str(text)
        self.fontSize = font
        self.font = Fonts.fonts[font]
        self.color = color
        self.pos = position
        self.centered = centered
        self.text = self.font.render(self.content, True, self.color)
        self.rect = pygame.Rect(0,0,0,0)
        Text.texts.append(self)
        self.underline = underline

    def resize(self):
        self.font = Fonts.fonts[self.fontSize]
        self.text = self.font.render(self.content, True, self.color)

    def reset(self, color, content):
        self.color = color
        self.content = content
        self.font = Fonts.fonts[self.fontSize]
        self.text = self.font.render(self.content, True, self.color)
    
    def setPosition(self, pos):
        self.pos = pos

    def draw(self, surface, noPercent=False):
        if not noPercent:
            if self.centered:
                self.rect = pygame.Rect(surface.get_width()/100*self.pos[0]-self.text.get_width()/2, surface.get_height()/100*self.pos[1], self.text.get_width(), self.text.get_height())
                surface.blit(self.text, (surface.get_width()/100*self.pos[0]-self.text.get_width()/2, surface.get_height()/100*self.pos[1]))
            else:
                self.rect = pygame.Rect(surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1], self.text.get_width(), self.text.get_height())
                surface.blit(self.text, (surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1]))
        else:
            if self.centered:
                self.rect = pygame.Rect(self.pos[0]-self.text.get_width()/2, self.pos[1], self.text.get_width(), self.text.get_height())
                surface.blit(self.text, (self.pos[0]-self.text.get_width()/2, self.pos[1]))
            else:
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.text.get_width(), self.text.get_height())
                surface.blit(self.text, (self.pos[0], self.pos[1]))
        


    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def resizeAll(surface):
        Fonts.resizeFonts(surface)
        for text in Text.texts:
            text.resize()


class Button:
    buttons = []
    def __init__(self, text, rect, cornerRadius, textColor=Colors.textCol, gradCol1=Colors.buttonCol1, gradCol2=Colors.buttonCol2, onclickFunc=None) -> None:
        self.rect: pygame.Rect = rect
        self.convertedRect = convertRect((self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        self.surface = pygame.Surface((self.convertedRect.width, self.convertedRect.height), pygame.SRCALPHA)
        self.hoverSurface = pygame.Surface((self.convertedRect.width, self.convertedRect.height), pygame.SRCALPHA)
        self.textContent = text
        self.textColor = textColor
        self.cornerRadius = cornerRadius
        self.gradCol1 = gradCol1
        self.gradCol2 = gradCol2
        self.hovering = False
        self.onClickFunc = onclickFunc
        self.drawImage(self.gradCol1, self.gradCol2, self.textColor, self.surface)
        self.drawImage(self.darken(self.gradCol1, .9), self.darken(self.gradCol2, .9), self.darken(self.textColor, .9), self.hoverSurface)
        self.resizedSurface = pygame.transform.scale(self.surface, (self.convertedRect.width, self.convertedRect.height))
        self.resizedHoverSurface = pygame.transform.scale(self.hoverSurface, (self.convertedRect.width, self.convertedRect.height))

        Button.buttons.append(self)

    def drawImage(self, gradCol1, gradCol2, textCol, surface):
        color = gradCol1.copy()
        inc1 = (gradCol2[0] - gradCol1[0])/(self.convertedRect.height - self.cornerRadius)
        inc2 = (gradCol2[1] - gradCol1[1])/(self.convertedRect.height - self.cornerRadius)
        inc3 = (gradCol2[2] - gradCol1[2])/(self.convertedRect.height - self.cornerRadius)
        for i in range(self.convertedRect.height - self.cornerRadius):
            pygame.draw.rect(surface, color, pygame.Rect(0, i, self.convertedRect.width, self.cornerRadius), border_radius=self.cornerRadius)
            color[0] += inc1
            color[1] += inc2
            color[2] += inc3
        text = Fonts.fonts["button"].render(self.textContent, True, textCol)
        surface.blit(text, (surface.get_width()/2-text.get_width()/2, surface.get_height()/2-text.get_height()/2))

    def darken(self, color, val):
        newCol = color.copy()
        newCol = [clampColor(newCol[0] * val), clampColor(newCol[1] * val), clampColor(newCol[2] * val)]
        return newCol

    def draw(self, surface):
        if self.hovering == False:
            surface.blit(self.resizedSurface, (self.convertedRect.x, self.convertedRect.y))
        else:
            surface.blit(self.resizedHoverSurface, (self.convertedRect.x, self.convertedRect.y))

    def checkMouseOver(self, pos):
        if self.convertedRect.collidepoint(pos):
            return True

    def resize(self, surface):
        self.convertedRect = convertRect(surface, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        self.resizedSurface = pygame.transform.scale(self.surface, (self.convertedRect.width, self.convertedRect.height))
        self.resizedHoverSurface = pygame.transform.scale(self.hoverSurface, (self.convertedRect.width, self.convertedRect.height))

class PixelButton:
    def __init__(self, rect, message, col1, col2, icon=None) -> None:
        self.pixelSize = 7
        self.hasIcon = False
        if icon != None:
            self.hasIcon = True
            self.iconImg = pygame.image.load(icon)
            self.iconImg = pygame.transform.scale(self.iconImg, (self.iconImg.get_width()*3, self.iconImg.get_height()*3))
        if message == None:
            self.hasMessage = False
        else:
            self.hasMessage = True
            self.text = Text(message, "button2", (255,255,255), (50, 0), True)
            self.text2 = Text(message, "button2", (255*.8,255*.8,255*.8), (50, 0), True)
        self.rect = pygame.Rect(rect.x,rect.y, 5*(rect.w//5), 5*(rect.h//5))
        self.surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.darkenedSurf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.col1 = col1
        self.col2 = col2
        self.drawButton()

    def drawButton(self):
        pygame.draw.rect(self.surf, self.col2, pygame.Rect(self.pixelSize,0, self.rect.w-2*self.pixelSize,self.pixelSize+1))
        pygame.draw.rect(self.surf, self.col2, pygame.Rect(self.pixelSize,self.rect.h-self.pixelSize-1, self.rect.w-2*self.pixelSize,self.pixelSize+1))
        pygame.draw.rect(self.surf, self.col2, pygame.Rect(0, self.pixelSize, self.pixelSize+1, self.rect.h-2*self.pixelSize))
        pygame.draw.rect(self.surf, self.col2, pygame.Rect(self.rect.w-self.pixelSize-1, self.pixelSize, self.pixelSize+1, self.rect.h-2*self.pixelSize))
        pygame.draw.rect(self.surf, self.col1, pygame.Rect(self.pixelSize, self.pixelSize, self.rect.width-2*self.pixelSize, self.rect.height-2*self.pixelSize))
        if self.hasMessage:
            self.text.draw(self.surf)
        if self.hasIcon:
            self.surf.blit(self.iconImg, (self.surf.get_width()/2-self.iconImg.get_width()/2, self.surf.get_height()/2-self.iconImg.get_height()/2))

        self.col3 = (self.col1[0]*.8, self.col1[1]*.8, self.col1[2]*.8)
        self.col4 = (self.col2[0]*.8, self.col2[1]*.8, self.col2[2]*.8)
        pygame.draw.rect(self.darkenedSurf, self.col4, pygame.Rect(self.pixelSize,0, self.rect.w-2*self.pixelSize,self.pixelSize+1))
        pygame.draw.rect(self.darkenedSurf, self.col4, pygame.Rect(self.pixelSize,self.rect.h-self.pixelSize-1, self.rect.w-2*self.pixelSize,self.pixelSize+1))
        pygame.draw.rect(self.darkenedSurf, self.col4, pygame.Rect(0, self.pixelSize, self.pixelSize+1, self.rect.h-2*self.pixelSize))
        pygame.draw.rect(self.darkenedSurf, self.col4, pygame.Rect(self.rect.w-self.pixelSize-1, self.pixelSize, self.pixelSize+1, self.rect.h-2*self.pixelSize))
        pygame.draw.rect(self.darkenedSurf, self.col3, pygame.Rect(self.pixelSize, self.pixelSize, self.rect.width-2*self.pixelSize, self.rect.height-2*self.pixelSize))
        if self.hasMessage:
            self.text2.draw(self.darkenedSurf)
        if self.hasIcon:
            self.icon2 = self.iconImg.copy()
            self.icon2.set_alpha(255*.6)
            self.darkenedSurf.blit(self.icon2, (self.surf.get_width()/2-self.icon2.get_width()/2, self.surf.get_height()/2-self.icon2.get_height()/2))

    def render(self, screen):
        if not self.hovering():
            screen.blit(self.surf, self.rect.topleft)
        else:
            screen.blit(self.darkenedSurf, self.rect.topleft)

    def hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def update(self):
        pass

# A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, grid):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current_node
            neighbor = x + dx, y + dy

            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and not grid[neighbor[1]][neighbor[0]]:
                new_cost = cost_so_far[current_node] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current_node

    return None
