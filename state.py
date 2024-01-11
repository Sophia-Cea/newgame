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
        self.inventoryButton = PixelButton(pygame.Rect(940,90, 40,40), "i", (87,32,254), (11,69,255))
        self.toolIcons = ["gun", "shovel", "pickaxe", "rocket"]
        for i in range(len(self.toolIcons)):
            self.toolIcons[i] = PixelButton(pygame.Rect(740+i*65, 640, 55,55), None, (200,160,255), (180,120,200), "assets/icons/" + self.toolIcons[i] + ".png")
        self.fuelBar = pygame.transform.scale_by(pygame.image.load("assets/icons/fuelBar.png"), 5)
        

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
        self.inventoryButton.render(screen)
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
        
        pygame.draw.rect(screen, (0,140,90), pygame.Rect(385,30,250*(world.fuel/world.requiredFuel*.925), 25))
        screen.blit(self.fuelBar, (375,25))

    def update(self):
        super().update()
        player.update()
        camera.update()
        world.update()
        for enemy in Level1.enemies:
            enemy.update()
        self.texts[0].reset(self.textColor, str(player.money))
        if player.health == 0:
            stateManager.pop()
            stateManager.push(GameOverState())
        for enemy in Level1.enemies:
            if enemy.health <= 0:
                Level1.enemies.remove(enemy)
        
        if world.checkPlayerWon(player):
            # global world
            # world = Level2(2)
            FadeOutState()

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
                if self.inventoryButton.hovering():
                    stateManager.push(InventoryState())
    

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

class ShopItem:
    def __init__(self, title, price, icon, memo=None) -> None:
        self.title = title
        self.price = price
        self.icon = icon
        self.icon = pygame.transform.scale(self.icon, (self.icon.get_width()*4, self.icon.get_height()*4))
        self.memo = memo
        self.titleText = Text(self.title, "shopText", (255,255,255), (0,0), False) 
        self.priceText = Text(self.price, "shopText2", (255,255,255), (0,0), False)
        self.memoTexts = []
        for item in self.memo:
            self.memoTexts.append(Text(item, "shopText2", (255,255,255), (0,0), False))
        self.rect = pygame.Rect(0,0,360,85)
        self.bought = False
        self.boughtSign = pygame.transform.scale_by(pygame.image.load("assets/icons/soldIcon.png"), 3)
        # upgrading will be just replacing the item until its at a maximum level


    def render(self, screen, pos):
        self.rect.x = pos[0]-5
        self.rect.y = pos[1]-5
        pygame.draw.rect(screen, (80, 230,230), pygame.Rect(pos[0], pos[1], 75,75), 5)
        screen.blit(self.icon, pos)

        self.titleText.setPosition((pos[0]+85, pos[1]-5))
        self.priceText.setPosition((pos[0]+85, pos[1]+20))
        i=0
        for item in self.memoTexts:
            item.setPosition((pos[0]+85, pos[1]+40+i*16))
            item.draw(screen, True)
            i += 1
        self.titleText.draw(screen, True)
        self.priceText.draw(screen, True)
        if self.bought:
            self.boughtSign2 = pygame.transform.rotate(self.boughtSign, -10)
            screen.blit(self.boughtSign2, (pos[0]-10,pos[1]+10))

class ShopState(State):
    shopItems = [
            ShopItem("Explosive Blast", 50, pygame.image.load("assets/icons/rocket.png"), ["explode blocks within 3", "block radius."]), 
            ShopItem("Stronger Blast", 100, pygame.image.load("assets/ingredients/fireEssence.png"), ["Increase radius of blast by", "1 block."]),
            ShopItem("Vision Upgrade", 80, pygame.image.load("assets/ingredients/magicMushroom.png"), ["Increase vision radius by", "3 blocks for 15 seconds"]),
            ShopItem("Stronger Attack", 60, pygame.image.load("assets/icons/gun.png"), ["Increase damage to enemies", "by 5 health points."])
        ]
    def __init__(self) -> None:
        super().__init__()
        self.pixelSize = 6
        self.menuBackground = pygame.Surface((self.pixelSize*(WIDTH*.4//self.pixelSize), self.pixelSize*(HEIGHT*.8//self.pixelSize))) #, pygame.SRCALPHA)
        self.rect = pygame.Rect(30, (HEIGHT-self.menuBackground.get_height())/2, self.menuBackground.get_width(), self.menuBackground.get_height())
        self.popupBg = pygame.Surface((WIDTH*.4,HEIGHT*.4), pygame.SRCALPHA)
        self.drawMenu(self.menuBackground)
        self.drawMenu(self.popupBg)
        self.exitButton2 = PixelButton(pygame.Rect(290,170,35,35), "x", (150,120,135), (100,70,80))
        self.exitButton = PixelButton(pygame.Rect(30,70,35,35), "x", (150,120,135), (100,70,80))
        self.texts = [Text("Shop", "subtitle", (255,255,255), (18,11), True)]
        self.backgroundCover = pygame.Surface((WIDTH,HEIGHT)).convert()
        self.backgroundCover.set_alpha(150)
        self.prompting = False
        self.promptTexts = [
            Text("Would you like to purchase", "shopText", (255,255,255), (50,28), True), 
            Text("yee", "shopText", (255,255,255), (50,31), True),
            Text("for ###?", "shopText", (255,255,255), (50,34), True)
        ]
        self.purchaseButton = PixelButton(pygame.Rect(450,320,100,50), "buy", (223,32,133), (123,231,123))
        self.tooPoorSign = pygame.transform.scale_by(pygame.image.load("assets/icons/lackoffunds.png"), 4.5)
    
    def drawMenu(self, surf):
        pygame.draw.rect(surf, (60,60,80), pygame.Rect(self.pixelSize*2,0,surf.get_width()-4*self.pixelSize, surf.get_height()))
        pygame.draw.rect(surf, (60,60,80), pygame.Rect(0,self.pixelSize*2, surf.get_width(), surf.get_height()-4*self.pixelSize))
        pygame.draw.rect(surf, (60,60,80), pygame.Rect(self.pixelSize, self.pixelSize, surf.get_width()-2*self.pixelSize, surf.get_height()-2*self.pixelSize))
        pygame.draw.rect(surf, (130,130,160), pygame.Rect(self.pixelSize*3, self.pixelSize*2, surf.get_width()-6*self.pixelSize, surf.get_height()-4*self.pixelSize))
        pygame.draw.rect(surf, (130,130,160), pygame.Rect(self.pixelSize*2, self.pixelSize*3, surf.get_width()-4*self.pixelSize, surf.get_height()-6*self.pixelSize))


    def render(self, screen):
        super().render(screen)
        screen.blit(self.backgroundCover, (0,0))
        screen.blit(self.menuBackground, self.rect.topleft)
        self.exitButton.render(screen)
        for text in self.texts:
            text.draw(screen)
        i = 0
        for item in ShopState.shopItems:
            item.render(screen, (50, 145+i*90))
            if not self.prompting and item.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 60, 210), item.rect, 3)
            i += 1
        if self.prompting:
            screen.blit(self.popupBg, (WIDTH*.3, HEIGHT*.25))
            for text in self.promptTexts:
                text.draw(screen)
            self.exitButton2.render(screen)
            if player.money < self.currentItem.price:
                self.tooPoorSign2 = pygame.transform.rotate(self.tooPoorSign, 7)
                self.popupBg.blit(self.tooPoorSign2, (40,130))
            else:
                self.purchaseButton.render(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitButton.hovering():
                    stateManager.pop()
                
                i=0
                if not self.prompting:
                    for item in ShopState.shopItems:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            if not ShopState.shopItems[i].bought:
                                self.prompt(i)
                        i+=1
                else:
                    if self.exitButton2.hovering():
                        self.prompting = False
                    if self.purchaseButton.hovering():
                        if player.money >= self.currentItem.price:
                            player.money -= self.currentItem.price
                            self.prompting = False
                            self.currentItem.bought = True

    def prompt(self, itemNum):
        self.prompting = True
        self.currentItem = ShopState.shopItems[itemNum]
        self.promptTexts[1].reset((255,255,255), ShopState.shopItems[itemNum].title)
        self.promptTexts[2].reset((255,255,255), "for " + str(ShopState.shopItems[itemNum].price) + "?")

class CraftingState(State):
    def __init__(self) -> None:
        super().__init__()
        self.pixelSize = 6
        self.background = pygame.Surface((self.pixelSize*(WIDTH*.4//self.pixelSize), self.pixelSize*(HEIGHT*.5//self.pixelSize))) #, pygame.SRCALPHA)
        self.rect = pygame.Rect((WIDTH-self.background.get_width())/2, HEIGHT*.07, self.background.get_width(), self.background.get_height())
        self.drawMenu()
        self.backgroundCover = pygame.Surface((WIDTH,HEIGHT)).convert()
        self.backgroundCover.set_alpha(150)
        self.exitButton = PixelButton(pygame.Rect(290,40,35,35), "x", (150,120,135), (100,70,80))
        self.titleText = Text("Brewing", "title", (255,255,255), (50,12), True)
        self.itemBackground = pygame.Surface((60,60)).convert()
        self.itemBackground.fill((255,255,255))
        self.itemBackground.set_alpha(170)
        '''
        # self.potionBottles = {
        #     "empty" : pygame.image.load("assets/potions/empty.png"),
        #     "invincibility" : pygame.image.load("assets/potions/red.png"),
        #     "all seeing" : pygame.image.load("assets/potions/blue.png"),
        #     "invisibility" : pygame.image.load("assets/potions/midnight.png"),
        #     "big dig" : pygame.image.load("assets/potions/yellow.png"),
        #     "speed" : pygame.image.load("assets/potions/pink.png"),
        #     "confusion" : pygame.image.load("assets/potions/orange.png"),
        #     "poison" : pygame.image.load("assets/potions/green.png"),
        #     "health" : pygame.image.load("assets/potions/purple.png")
        # }
        self.potionIngredients = {
            "flameEssence" : pygame.image.load("assets/ingredients/fireEssence.png"),
            "shadowEssence" : pygame.image.load("assets/ingredients/shadowEssence.png"),
            "waterEssence" : pygame.image.load("assets/ingredients/waterEssence.png"),
            "flamePetals" : pygame.image.load("assets/ingredients/firePetals.png"),
            "glowingPetals" : pygame.image.load("assets/ingredients/glowingPetals.png"),
            "goldPetals" : pygame.image.load("assets/ingredients/goldPetals.png"),
            "icePetals" : pygame.image.load("assets/ingredients/icePetals.png"),
            # "glowingMushroom" : pygame.image.load("assets/ingredients/glowingMushroom.png"),
            "magicMushroom" : pygame.image.load("assets/ingredients/magicMushroom.png"),
            # "purpleMushroom" : pygame.image.load("assets/ingredients/purpleMushroom.png"),
            # "blueMushroom" : pygame.image.load("assets/ingredients/blueMushroom.png"),
            # "orangeMushroom" : pygame.image.load("assets/ingredients/orangeMushroom.png"),
            "bones" : pygame.image.load("assets/ingredients/bones.png"),
            "poisonGoo" : pygame.image.load("assets/ingredients/poisonGoo.png"),
            "lightCrystals" : pygame.image.load("assets/icons/crystal.png"),
            "soulStone" : pygame.image.load("assets/ingredients/soulStone.png"),
        }
        self.potionRecipes = {
            "invincibility" : ["bones", "soulStone", "fireEssence"],
            "all seeing" : ["lightCrystals", "fireEssence", "glowingPetals"],
            "invisibility" : ["shadowEssence", "magicMushroom", "goldPetals"],
            "big dig" : ["bones", "goldPetals", "orangeMushroom"],
            "speed" : ["waterEssence", "bones", "icePetal"],
            "confusion" : ["glowingMushroom", "flamePetals", "magicMushroom"],
            "poison" : ["posionGoo", "orangeMushroom", "magicPetals"],
            "health" : ["lightCrystals", "fireEssence", "mushroom"]
        }
        '''
        self.potions = {
            "empty" : pygame.image.load("assets/potions/empty.png"),
            "invincibility" : Potion(["bones", "soulStone", "fireEssence"], "red", "invincibility"),
            "all seeing" : Potion(["lightCrystals", "fireEssence", "glowingPetals"], "blue", "all seeing"),
            "invisibility" : Potion(["shadowEssence", "magicMushroom", "goldPetals"], "midnight", "invisibility"),
            "big dig" : Potion(["bones", "goldPetals", "orangeMushroom"], "yellow", "big dig"),
            "speed" : Potion(["waterEssence", "bones", "icePetal"], "pink", "speed"),
            "confusion" : Potion(["glowingMushroom", "flamePetals", "magicMushroom"], "orange", "confusion"),
            "poison" : Potion(["posionGoo", "orangeMushroom", "magicPetals"], "green", "poison"),
            "health" : Potion(["lightCrystals", "fireEssence", "mushroom"], "purple", "health")
        }
        self.emptyBottle = pygame.image.load("assets/potions/empty.png")
        self.emptyBottle = pygame.transform.scale(self.emptyBottle, (self.emptyBottle.get_width()*6, self.emptyBottle.get_height()*6))
        self.boxItems = [None, None, None]
        self.inventoryRects = []
        for i in range(4):
            for j in range(4):
                self.inventoryRects.append(pygame.Rect(335+j*90, 410+i*70, 60,60))
        self.draggingItem = False
        self.itemBeingDragged = None
        self.ingredientRects = []
        for i in range(3):
            self.ingredientRects.append(pygame.Rect(365+i*95,180,80,80))
        self.brewButton = PixelButton(pygame.Rect(570,300,100,45), "brew", (140,80,170), (100,50,130))
        self.currentPotion = None
        
    
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
        self.brewButton.render(screen)
        self.titleText.draw(screen)
        for rect in self.ingredientRects:
            pygame.draw.rect(screen, (60,60,80), rect, 8)

        pygame.draw.rect(screen, (60,60,80), pygame.Rect(455,280, 90,90), 8)
        for rect in self.inventoryRects:
            pygame.draw.rect(screen, (230,230,240), rect, 5)
            screen.blit(self.itemBackground, (rect.x, rect.y))

        i=0
        for item in player.inventory:
            if not self.draggingItem:
                item.render(screen, (342+90*(i%4), 420+70*(i//4)))
            else:
                if item == self.itemBeingDragged:
                    item.render(screen, pygame.mouse.get_pos())
                else:
                    item.render(screen, (342+90*(i%4), 420+70*(i//4)))
            i += 1
        
        i = 0
        for item in self.boxItems:
            if item != None:
                item.render(screen, (380+i*95,200))
            i += 1

        if None not in self.boxItems:
            boxItemStrList = []
            for item in self.boxItems:
                boxItemStrList.append(item.item)

            for potion in self.potions:
                boxItemStrList.sort()
                if potion != "empty":
                    if boxItemStrList == self.potions[potion].ingredients:
                        self.currentPotion = self.potions[potion]
                        self.potions[potion].render(screen, (472,290), 6)
                    else:
                        screen.blit(self.emptyBottle, (472,290))
        else:
            screen.blit(self.emptyBottle, (472,290))


    def update(self):
        super().update()
        if self.draggingItem:
            pos = pygame.mouse.get_pos()
            

    def handleInput(self, events):
        super().handleInput(events)
        for event in events: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.exitButton.hovering():
                    for item in self.boxItems:
                        if item != None:
                            player.inventory.append(item)
                    stateManager.pop()
                if self.brewButton.hovering():
                    player.inventory.append(self.currentPotion)
                    self.boxItems = [None, None, None]
                    self.currentPotion = None
                i = 0
                for rect in self.inventoryRects:
                    if rect.collidepoint(pos):
                        if i<len(player.inventory):
                            self.draggingItem = True
                            self.itemBeingDragged = player.inventory[i]
                    i += 1
            if event.type == pygame.MOUSEBUTTONUP:
                i=0
                if self.draggingItem:
                    for rect in self.ingredientRects:
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            if self.boxItems[i] != None:
                                player.inventory.append(self.boxItems[i])
                            self.boxItems[i] = self.itemBeingDragged
                            player.inventory.remove(self.itemBeingDragged)
                        i += 1
                    self.draggingItem = False
                    self.itemBeingDragged = None

class InventoryState(State):
    def __init__(self) -> None:
        super().__init__()
        self.inventoryRects = []
        for i in range(4):
            for j in range(4):
                self.inventoryRects.append(pygame.Rect(330+j*90, 200+i*90, 70,70))
        self.backgroundSurf = pygame.Surface((WIDTH,HEIGHT)).convert()
        self.backgroundSurf.set_alpha(200)
        self.inventoryBg = pygame.Surface((70,70)).convert()
        self.inventoryBg.fill((255,255,255))
        self.inventoryBg.set_alpha(140)
        self.exitButton = PixelButton(pygame.Rect(280, 160, 40,40), "x", (96,111,82), (200,150,150))


    def render(self, screen):
        screen.blit(self.backgroundSurf, (0,0))
        # pygame.draw.line(screen, (255,0,0), (WIDTH/2,0), (WIDTH/2,HEIGHT), 1)
        for rect in self.inventoryRects:
            screen.blit(self.inventoryBg, rect.topleft)
            pygame.draw.rect(screen, (255,255,255), rect, 5)
        self.exitButton.render(screen)
        i=0
        for item in player.inventory:
            item.render(screen, (340+90*(i%4), 213+90*(i//4)))
            i+=1

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitButton.hovering():
                    stateManager.pop()

class FadeOutState(State):
    def __init__(self, nextState=None) -> None:
        super().__init__()
        self.nextState = nextState
        self.fadeScreen = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.alphaVal = 0
        self.fadeScreen.set_alpha(self.alphaVal)
        self.timer = 100

    def render(self, screen):
        screen.blit(self.fadeScreen, (0,0))
    
    def update(self):
        super().update()
        if self.alphaVal < 255:
            self.alphaVal += 1
            self.fadeScreen.set_alpha(self.alphaVal)
        else:
            if self.timer > 0:
                self.timer -= 1
            else:
                stateManager.pop()
                # stateManager.push(self.nextState)
                stateManager.push(FadeInState())

class FadeInState(State):
    def __init__(self) -> None:
        super().__init__()
        self.fadeScreen = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.alphaVal = 255
        self.fadeScreen.set_alpha(self.alphaVal)

    def render(self, screen):
        screen.blit(self.fadeScreen, (0,0))
    
    def update(self):
        super().update()
        if self.alphaVal > 0:
            self.alphaVal -= 1
            self.fadeScreen.set_alpha(self.alphaVal)
        else:
            stateManager.pop()





                
    

