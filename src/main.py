# src/main.py

import pygame, sys
from src.ui.debug import debug
from src.ui.asset_manager import load_assets, ASSETS
from src.combat.domain.model.Player import Player

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('Team 9: Roguelike Auto Battler')
        self.clock = pygame.time.Clock()
        self.debug_mode = False

        # Load all graphic assets into memory
        load_assets()

        # Instantiate domain model
        self.player = Player(player_id=1, x=400.0, y=300.0, speed=250.0)

    def run(self):

        # main pygame loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # handle discrete key presses
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    # toggle global debug mode
                    if event.key == pygame.K_F2 and event.type == pygame.KEYDOWN:
                        self.debug_mode = not self.debug_mode
                        print(f"[INFO] Debug Mode: {self.debug_mode}")

            # delta time / tick
            dt = self.clock.tick(60) / 1000.0

            # handle continuous key presses
            keys = pygame.key.get_pressed()
            dx = float((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]))
            dy = float((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]))

            # update domain model
            self.player.move(dx, dy, dt)

            # rendering
            self.screen.fill('#71DDEE')
            player_surface = ASSETS['player_idle'][0][0]
            # pygame.draw.rect(self.screen, (230, 50, 50), (int(self.player.x), int(self.player.y), 32, 32))
            self.screen.blit(player_surface, (int(self.player.x), int(self.player.y)))
            if self.debug_mode:
                x = pygame.display.get_surface().get_size()[0] - 100
                debug('fps: ' + str(int(self.clock.get_fps())), x, 20)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()