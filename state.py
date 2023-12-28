from enemy import *


class StateManager:
    def __init__(self) -> None:
        self.queue = []

    def push(self, page):
        self.queue.append(page)
        page.onEnter()

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)

    def run(self, surface, events):
        self.queue[len(self.queue)-1].update()
        if len(self.queue) > 1:
            self.queue[len(self.queue)-2].render(surface)
        self.queue[len(self.queue)-1].render(surface)
        self.queue[len(self.queue)-1].handleInput(events)

stateManager = StateManager()

class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass



class PlayState(State):
    def __init__(self) -> None:
        super().__init__()
        Level1.enemies = [Patroller((38,26), 2, 5), Patroller((39,38), 1, 6), Patroller((58,29), 2, 7), Patroller((49,32), 1, 4), Explorer((41,34)), Explorer((8,30)), Explorer((29,28)), Explorer((58,10)), Explorer((50,23))]
        self.textColor = (180,100,200)
        self.texts = [Text(str(player.money), "button2", self.textColor, (91,1), False)]
        self.menuButton = PixelButton(pygame.Rect(20,20,40,40), "<", (150,150,160), (80,80,100))
        self.heartIcon = pygame.image.load("assets/icons/heart.png")
        self.heartIcon = pygame.transform.scale(self.heartIcon, (self.heartIcon.get_width()*4, self.heartIcon.get_height()*4))
        self.heartIconTransparent = self.heartIcon.copy().convert()
        self.crystalIcon = pygame.image.load("assets/icons/crystal.png")
        self.crystalIcon = pygame.transform.scale(self.crystalIcon, (self.crystalIcon.get_width()*4, self.crystalIcon.get_height()*4))
        self.shopButton = PixelButton(pygame.Rect(70, 20, 40,40), ".", (170,150,150), (100,80,80))
        self.craftingButton = PixelButton(pygame.Rect(120, 20, 40,40), "/", (200,150,180), (130,80,100))
        self.toolIcons = ["gun", "shovel", "pickaxe", "rocket"]
        for i in range(len(self.toolIcons)):
            self.toolIcons[i] = PixelButton(pygame.Rect(740+i*65, 640, 55,55), None, (200,160,255), (180,120,200), "assets/icons/" + self.toolIcons[i] + ".png")
        

    def render(self, screen):
        super().render(screen)
        screen.fill((0,0,0))
        world.render(screen, player.playerGridPos())
        player.render(screen)
        for enemy in Level1.enemies:
            enemy.render(screen)
        for text in self.texts:
            text.draw(screen)
        screen.blit(self.crystalIcon, (880,15))
        self.menuButton.render(screen)
        self.shopButton.render(screen)
        self.craftingButton.render(screen)
        i = 0
        for button in self.toolIcons:
            button.render(screen)
            if i == player.currentTool:
                pygame.draw.rect(screen, (80,60,230), pygame.Rect(740+i*65, 640, 55,55), 5)
            i += 1

        if player.health%20 == 0:
            transparentHeart = False
        else:
            transparentHeart = True
        for i in range(player.health//20):
            if transparentHeart:
                screen.blit(self.heartIcon, (WIDTH-(self.heartIcon.get_width()+5)*(player.health//20+1)-10+(self.heartIcon.get_width()+5)*i,50))
                screen.blit(self.heartIconTransparent, (WIDTH-15-self.heartIconTransparent.get_width(), 50))
            else:
                screen.blit(self.heartIcon, (WIDTH-(self.heartIcon.get_width()+5)*(player.health//20)-10+(self.heartIcon.get_width()+5)*i,50))
        if transparentHeart:
            # self.heartIconTransparent.set_alpha(255/(20-abs(player.health%20)+.0001))
            self.heartIconTransparent.set_alpha(12.75*abs(player.health%20))
            screen.blit(self.heartIconTransparent, (WIDTH-15-self.heartIconTransparent.get_width(), 50))

    def update(self):
        super().update()
        player.update()
        camera.update()
        for enemy in Level1.enemies:
            enemy.update()
        self.texts[0].reset(self.textColor, str(player.money))
        if player.health == 0:
            stateManager.pop()
            stateManager.push(GameOverState())
        for enemy in Level1.enemies:
            if enemy.health <= 0:
                Level1.enemies.remove(enemy)

    def handleInput(self, events):
        super().handleInput(events)
        player.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menuButton.hovering():
                    stateManager.push(MenuState())
                if self.shopButton.hovering():
                    stateManager.push(ShopState())
                if self.craftingButton.hovering():
                    stateManager.push(CraftingState())

class MenuState(State):
    def __init__(self) -> None:
        super().__init__()
        self.pixelSize = 6
        self.menuBackground = pygame.Surface((self.pixelSize*(WIDTH*.7//self.pixelSize), self.pixelSize*(HEIGHT*.7//self.pixelSize)), pygame.SRCALPHA)
        self.rect = pygame.Rect((WIDTH-self.menuBackground.get_width())/2, (HEIGHT-self.menuBackground.get_height())/2, self.menuBackground.get_width(), self.menuBackground.get_height())
        self.drawMenu()
        self.exitButton = PixelButton(pygame.Rect(136,97,35,35), "x", (150,120,135), (100,70,80))
        self.texts = [Text("Menu", "title", (255,255,255), (50,18), True)]
        self.buttons = [PixelButton(pygame.Rect(460, 350, 80,40), "Exit Game", (150,120,135), (100,70,80))]

    def drawMenu(self):
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(self.pixelSize*2,0,self.menuBackground.get_width()-4*self.pixelSize, self.menuBackground.get_height()))
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(0,self.pixelSize*2, self.menuBackground.get_width(), self.menuBackground.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(self.pixelSize, self.pixelSize, self.menuBackground.get_width()-2*self.pixelSize, self.menuBackground.get_height()-2*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (130,130,160), pygame.Rect(self.pixelSize*3, self.pixelSize*2, self.menuBackground.get_width()-6*self.pixelSize, self.menuBackground.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (130,130,160), pygame.Rect(self.pixelSize*2, self.pixelSize*3, self.menuBackground.get_width()-4*self.pixelSize, self.menuBackground.get_height()-6*self.pixelSize))


    def render(self, screen):
        super().render(screen)
        screen.blit(self.menuBackground, self.rect.topleft)
        self.exitButton.render(screen)
        for text in self.texts:
            text.draw(screen)
        for button in self.buttons:
            button.render(screen)

    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitButton.hovering():
                    stateManager.pop()

class GameOverState(State):
    def __init__(self) -> None:
        super().__init__()
        self.gameOverText = Text("Game Over", "title", (255,255,255), (50,35), True)
        self.gameOverText.text.convert()
        self.textOpacity = 0
        self.gameOverText.text.set_alpha(self.textOpacity)
        self.counter = 0
        self.timeDelay = 80

    def render(self, screen):
        screen.fill((0,0,0))
        self.gameOverText.draw(screen)
    
    def update(self):
        if self.counter < self.timeDelay:
            self.counter += 1
        else:
            if self.textOpacity < 255:
                self.textOpacity += 1
                self.gameOverText.text.set_alpha(self.textOpacity)

class ShopState(State):
    def __init__(self) -> None:
        super().__init__()
        self.pixelSize = 6
        self.menuBackground = pygame.Surface((self.pixelSize*(WIDTH*.3//self.pixelSize), self.pixelSize*(HEIGHT*.8//self.pixelSize)), pygame.SRCALPHA)
        self.rect = pygame.Rect(30, (HEIGHT-self.menuBackground.get_height())/2, self.menuBackground.get_width(), self.menuBackground.get_height())
        self.drawMenu()
        self.exitButton = PixelButton(pygame.Rect(30,70,35,35), "x", (150,120,135), (100,70,80))
        self.texts = [Text("Shop", "subtitle", (255,255,255), (18,11), True)]
        self.backgroundCover = pygame.Surface((WIDTH,HEIGHT)).convert()
        self.backgroundCover.set_alpha(150)
        self.shopItems = []
    
    def drawMenu(self):
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(self.pixelSize*2,0,self.menuBackground.get_width()-4*self.pixelSize, self.menuBackground.get_height()))
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(0,self.pixelSize*2, self.menuBackground.get_width(), self.menuBackground.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (60,60,80), pygame.Rect(self.pixelSize, self.pixelSize, self.menuBackground.get_width()-2*self.pixelSize, self.menuBackground.get_height()-2*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (130,130,160), pygame.Rect(self.pixelSize*3, self.pixelSize*2, self.menuBackground.get_width()-6*self.pixelSize, self.menuBackground.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.menuBackground, (130,130,160), pygame.Rect(self.pixelSize*2, self.pixelSize*3, self.menuBackground.get_width()-4*self.pixelSize, self.menuBackground.get_height()-6*self.pixelSize))


    def render(self, screen):
        super().render(screen)
        screen.blit(self.backgroundCover, (0,0))
        screen.blit(self.menuBackground, self.rect.topleft)
        self.exitButton.render(screen)
        for text in self.texts:
            text.draw(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitButton.hovering():
                    stateManager.pop()

class CraftingState(State):
    def __init__(self) -> None:
        super().__init__()
        self.pixelSize = 6
        self.background = pygame.Surface((self.pixelSize*(WIDTH*.5//self.pixelSize), self.pixelSize*(HEIGHT*.8//self.pixelSize)), pygame.SRCALPHA)
        self.rect = pygame.Rect(WIDTH/4, (HEIGHT-self.background.get_height())/2, self.background.get_width(), self.background.get_height())
        self.drawMenu()
        self.backgroundCover = pygame.Surface((WIDTH,HEIGHT)).convert()
        self.backgroundCover.set_alpha(150)
        self.exitButton = PixelButton(pygame.Rect(WIDTH/4-5,65,35,35), "x", (150,120,135), (100,70,80))
        self.titleText = Text("Brewing", "title", (255,255,255), (50,12), True)

    def drawMenu(self):
        pygame.draw.rect(self.background, (60,60,80), pygame.Rect(self.pixelSize*2,0,self.background.get_width()-4*self.pixelSize, self.background.get_height()))
        pygame.draw.rect(self.background, (60,60,80), pygame.Rect(0,self.pixelSize*2, self.background.get_width(), self.background.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.background, (60,60,80), pygame.Rect(self.pixelSize, self.pixelSize, self.background.get_width()-2*self.pixelSize, self.background.get_height()-2*self.pixelSize))
        pygame.draw.rect(self.background, (130,130,160), pygame.Rect(self.pixelSize*3, self.pixelSize*2, self.background.get_width()-6*self.pixelSize, self.background.get_height()-4*self.pixelSize))
        pygame.draw.rect(self.background, (130,130,160), pygame.Rect(self.pixelSize*2, self.pixelSize*3, self.background.get_width()-4*self.pixelSize, self.background.get_height()-6*self.pixelSize))


    def render(self, screen):
        super().render(screen)
        screen.blit(self.backgroundCover, (0,0))
        screen.blit(self.background, self.rect.topleft)
        self.exitButton.render(screen)
        self.titleText.draw(screen)
        # for text in self.texts:
        #     text.draw(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitButton.hovering():
                    stateManager.pop()
                
    

