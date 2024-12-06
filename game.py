import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        # Main character
        self.speed = 2
        self.movement = [False, False]
        self.cropped_region = (0, 20, 14, 28)
        self.assets = {
            'player': load_image('Hero.png')
        }
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

    def run(self):
        while True:
            self.screen.fill((10, 100, 100))

            cropped_width = self.cropped_region[2]
            cropped_height = self.cropped_region[3]

            self.player.update((self.movement[1]- self.movement[0], 0))
            self.player.render(self.screen, self.cropped_region)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)



Game().run()


