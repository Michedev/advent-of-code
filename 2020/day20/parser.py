from typing import List
import re

import numpy as np

TILEID_RE = re.compile(r'Tile (\d+):')


class Tile:

    def __init__(self, tileid, tilemap: np.array):
        self.tileid = tileid
        self.tilemap: np.ndarray = tilemap

    def rotate_180(self):
        return Tile(self.tileid, np.flip(self.tilemap))


def parse(text: str) -> List[Tile]:
    tileid = None
    tilemap = []
    result = []
    for line in text.split('\n'):
        if tileid is None:
            tileid = TILEID_RE.match(line).group(1)
            tileid = int(tileid)
        elif line is '':
            tilemap = np.array(tilemap)
            result.append(Tile(tileid, tilemap))
            tileid = None
            tilemap = []
        else:
            tilemap.append([x == '#' for x in line])
    return result