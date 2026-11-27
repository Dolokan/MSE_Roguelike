import pygame, sys

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('Team 9: Roguelike Auto Battler')
        self.clock = pygame.time.Clock()

    def run(self):

        # main pygame loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('#71DDEE')
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()