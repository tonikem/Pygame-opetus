import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_tile_images
from scripts.tilemap import Tilemap

TILE_SIZE = 24  # 32


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

        loaded_hero_img = load_image('Hero.png')
        hero_subsurface = loaded_hero_img.subsurface((0, 20, 14, 28))
        hero = pygame.transform.scale(hero_subsurface, (14, 28))

        self.assets = {
            'tiles': load_tile_images(tile_size=TILE_SIZE),
            'player': hero
        }

        self.player = PhysicsEntity(self, 'player', (250, 20), (14, 28))
        self.tilemap = Tilemap(self, tile_size=TILE_SIZE)

    def run(self):
        while True:
            self.display.fill((10, 100, 100))

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, self.cropped_region)

            # tile_images = load_tile_images()
            # self.display.blit(tile_images[80], (0, 0))

            # print(self.tilemap.tiles_around(self.player.pos))
            # print(self.tilemap.physics_rects_around(self.player.pos))

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


