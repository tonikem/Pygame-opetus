class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        _range = 10
        for i in range(_range):
            self.tilemap[str(3 + i) + f';{_range}'] = {'type': 'tiles', 'variant': 80, 'pos': (3 + i, _range)}
            self.tilemap[f'{_range};' + str(5 + i)] = {'type': 'tiles', 'variant': 81, 'pos': (_range, i + 5)}

    def render(self, surf):
        for tile in self.offgrid_tiles:
            variant = self.game.assets[tile['type']][tile['variant']]
            surf.blit(variant, tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            variant = self.game.assets[tile['type']][tile['variant']]
            surf.blit(variant, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

