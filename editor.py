import sys
import pygame

from scripts.utils import *
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
TILE_SIZE = 28 # 32
MAP_NAME = 'map.json'


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

        try:
            self.tilemap.load(MAP_NAME)
        except FileNotFoundError:
            pass  # Ohitetaan, jos tiedostoa ei löydy

        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.on_grid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets['tiles'][self.tile_variant].copy()
            current_tile_img.set_alpha(100) #  255 täysi

            # Hiiren kohta (skaalattu)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos_0 = int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size)
            tile_pos_1 = int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size)
            tile_pos = (tile_pos_0, tile_pos_1)

            if self.on_grid:
                x = tile_pos_0 * self.tilemap.tile_size - self.scroll[0]
                y = tile_pos_1 * self.tilemap.tile_size - self.scroll[1]
                self.display.blit(current_tile_img, (x, y))
            else:
                self.display.blit(current_tile_img, mouse_pos)

            # Tiilien asettelu hiiren painikkeilla
            if self.clicking and self.on_grid:
                self.tilemap.tilemap[str(tile_pos_0) + ';' + str(tile_pos_1)] = {
                    'type': 'tiles',
                    'variant': self.tile_variant,
                    'pos': tile_pos
                }
            if self.right_clicking:
                tile_loc = str(tile_pos_0) + ';' + str(tile_pos_1)
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

                # Offgrid tiilien poistaminen
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets['tiles'][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            #self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            tile = {
                                'type': 'tile',
                                'variant': self.tile_variant,
                                'pos': (
                                    mouse_pos[0] + self.scroll[0],
                                    mouse_pos[1] + self.scroll[1]
                                )
                            }
                            self.tilemap.offgrid_tiles.append(tile)

                    if event.button == 3:
                        self.right_clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

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

                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid

                    if event.key == pygame.K_s:
                        self.tilemap.save(MAP_NAME)

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


