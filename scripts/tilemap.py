import pygame
from Demos.mmapfile_demo import offset

NEIGHBOR_OFFSETS = [
    (-1,  0), (-1, -1), ( 0, -1),
    ( 1, -1), ( 1,  0), ( 0,  0),
    (-1,  1), ( 0,  1), ( 1,  1)
]

PHYSICS_TILES = {
    'tiles'
}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        #_range = 2
        #for i in range(_range):
        #    self.tilemap[str(3 + i) + f';{_range}'] = {'type': 'tiles', 'variant': 80, 'pos': (3 + i, _range)}
        #    self.tilemap[f'{_range};' + str(5 + i)] = {'type': 'tiles', 'variant': 81, 'pos': (_range, 5)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                pos0 = tile['pos'][0] * self.tile_size
                pos1 = tile['pos'][1] * self.tile_size
                rect = pygame.Rect(pos0, pos1, self.tile_size, self.tile_size)
                rects.append(rect)
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            variant = self.game.assets['tiles'][tile['variant']]
            surf.blit(variant, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (
                    tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        ##¤ Vanha koodi ¤##
        #for loc in self.tilemap:
        #    tile = self.tilemap[loc]
        #    variant = self.game.assets[tile['type']][tile['variant']]
        #    surf.blit(variant, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))


