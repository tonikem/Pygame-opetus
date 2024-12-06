import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_tile_images
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # Main character
        self.speed = 1
        self.movement = [False, False]
        self.cropped_region = (0, 20, 14, 28)
        self.assets = {
            'tiles': load_tile_images(),
            'player': load_image('Hero.png')
        }
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)

    def run(self):
        while True:
            self.display.fill((10, 100, 100))

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, self.cropped_region)

            # tile_images = load_tile_images()
            # self.display.blit(tile_images[80], (0, 0))

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

            scale = pygame.transform.scale(self.display, self.screen.get_size())
            self.screen.blit(scale, (0, 0))
            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    Game().run()


