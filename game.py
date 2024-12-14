import sys
import pygame

from editor import MAP_NAME
from scripts.entities import PhysicsEntity, Player
from scripts.utils import *
from scripts.tilemap import Tilemap

TILE_SIZE = 28 # 32
JUMP_FORCE = -3 # Täytyy olla negatiivinen


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")

        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/background.mp3")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play()

        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # Main character
        self.speed = 2
        self.movement = [False, False]

        hero_cropped_region = (0, 20, 14, 28)
        loaded_hero_img = load_image('Hero.png')
        hero_subsurface = loaded_hero_img.subsurface(hero_cropped_region )
        hero = pygame.transform.scale(hero_subsurface, (14, 28))

        self.assets = {
            'tiles': load_tile_images(tile_size=TILE_SIZE),
            'background': load_image("background.png"),
            'player': hero, # <- Ei animaatiota.
            'player/idle': Animation(load_hero_idle_images(), img_dur=6),
            'player/run': Animation(load_hero_run_images(), img_dur=4),
            'player/jump': Animation(load_hero_jump_images(), img_dur=4, loop=False)
        }

        self.player = Player(self, (100, 10), (14, 28))
        self.tilemap = Tilemap(self, tile_size=TILE_SIZE)

        # Tason lataaminen
        self.tilemap.load(MAP_NAME)

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                print(spawner['pos'], 'enemy')

        self.scroll = [0, 0]

    def run(self):
        while True:
            # Renderöidään tausta
            self.display.blit(self.assets['background'], (0, 0))
            #self.display.fill((10, 100, 100))

            # Kameran kohdistus
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Tiilien renderöinti
            self.tilemap.render(self.display, offset=render_scroll)

            # Pelaajan renderöinti
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            #print(self.tilemap.tiles_around(self.player.pos))
            #print(self.tilemap.physics_rects_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = self.speed
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = self.speed

                    if event.key == pygame.K_UP:
                        self.player.jump(JUMP_FORCE)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # Skaalataan pelikenttä
            scale = pygame.transform.scale(self.display, self.screen.get_size())

            # Renderöidään tausta
            self.screen.blit(scale, (0, 0))
            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    Game().run()


