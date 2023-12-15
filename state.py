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
        self.queue[len(self.queue)-1].render(surface)
        self.queue[len(self.queue)-1].handleInput(events)

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
        self.enemies = []
        # self.enemies = [Enemy(), Enemy(), Enemy()]

    def render(self, screen):
        super().render(screen)
        screen.fill((0,0,0))
        world.render(screen, player.playerGridPos())
        player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)

    def update(self):
        super().update()
        player.update()
        camera.update()
        for enemy in self.enemies:
            enemy.update()
        # pos = pygame.mouse.get_pos()
        # print("tile pos: ", int((pos[0]-camera.offset[0])/tileSize), int((pos[1]-camera.offset[1])/tileSize))

    def handleInput(self, events):
        super().handleInput(events)
        player.handleInput(events)
