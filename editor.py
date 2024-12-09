import sys
import pygame

from scripts.utils import *
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
TILE_SIZE = 28 # 32


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            'tiles': load_tile_images(tile_size=TILE_SIZE),
        }
        self.movement = [False, False, False, False]
        self.tilemap = Tilemap(self, tile_size=TILE_SIZE)
        self.scroll = [0, 0]

        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            current_tile_img = self.assets['tiles'][self.tile_variant].copy()
            current_tile_img.set_alpha(100) #  255 täysi

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True

                if event.type == pygame.MOUSEWHEEL:
                    if event.y == 1:
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets['tiles'])
                    if event.y == -1:
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets['tiles'])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            # Skaalataan pelikenttä
            scale = pygame.transform.scale(self.display, self.screen.get_size())

            # Renderöidään tausta
            self.screen.blit(scale, (0, 0))
            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    Editor().run()


