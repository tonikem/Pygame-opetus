class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        _range = 10
        for i in range(_range):
            self.tilemap[str(3 + 1) + f';{_range}'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap[f'{_range};' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, i + 5)}

