from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Union
from path import Path
from numpy import array
from itertools import combinations, combinations_with_replacement, product, chain
from grid import GridND as GridNDCython

class Point:
    max_dims: int = 1000

    def __init__(self, *coordinates):
        self.c = tuple(coordinates)
        assert len(self.c) <= self.max_dims

    def __op(self, other, opf):
        if isinstance(other, (int, float)):
            return Point(*[opf(x, other) for x in self.c])
        return Point(*[opf(self.c[i], other.c[i]) for i in range(len(self.c))])

    def __add__(self, other):
        return self.__op(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.__op(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self.__op(other, lambda a, b: a * b)

    def __div__(self, other):
        return self.__op(other, lambda a, b: a / b)

    def __hash__(self):
        return sum(1000 ** i * self.c[i] for i in range(len(self.c)))

    def __len__(self): return len(self.c)

    def __getitem__(self, item): return self.c[item]

    def __repr__(self): return repr(self.c)

    def __iter__(self): return iter(self.c)


class GridND:

    def __init__(self, data_p: Union[dict, str], ndims: int = 3):
        Point.max_dims = ndims
        self.ndims = ndims
        if isinstance(data_p, str):
            self.data = self.parse_data(data_p)
        else:
            self.data = data_p
        self.variations1 = [Point(*d1) for d1 in product(range(-1, 2), repeat=ndims) if not all(x == 0 for x in d1)]
        self.variations2 = [Point(*d2) for d2 in product(range(-2, 3, 2), repeat=ndims) if not all(x == 0 for x in d2)]

    def parse_data(self, input_path: str):
        data = {}
        with open(input_path) as f:
            for i, line in enumerate(f.read().split('\n')):
                line_state = {}
                data[i] = line_state
                for j, el in enumerate(line):
                    assert el in ['.', '#']
                    is_active = el == '#'
                    if self.ndims == 3:
                        data[i][j] = [0] if is_active else []
                    elif self.ndims == 4:
                        x = [0] if is_active else []
                        data[i][j] = {0: x}
                    else:
                        raise ValueError(f'{self.ndims = } not supported')
        return data

    def is_active(self, p: array):
        data = self.data
        for dim in range(self.ndims - 1):
            i = p[dim]
            if i not in data: return False
            data = data[i]
        return p[-1] in data

    def iter_actives(self):
        if self.ndims == 3:
            for i in self.data:
                for j in self.data[i]:
                    for k in self.data[i][j]:
                        yield Point(i, j, k)
            return
        elif self.ndims == 4:
            for i in self.data:
                for j in self.data[i]:
                    for k in self.data[i][j]:
                        for l in self.data[i][j][k]:
                            yield Point(i, j, k, l)
            return
        # dimension variable version doesn't work so i wrote above this explicit version
        acc = []
        for i in self.data:
            acc +=  self.__iter_actives_rec(self.data, i, [i])
        return acc

    def __iter_actives_rec(self, data, i: int, prev):
        if isinstance(data[i], list):
            for x in data[i]:
                return [Point(*copy(prev + [x]))]
        acc = []
        for el in data[i]:
            if isinstance(el, list):
                for x in el:
                    return [Point(*copy(prev + [x]))]
            else:
                acc += self.__iter_actives_rec(data[i], el, copy(prev + [el]))
        return acc

    def _iter_neightbors(self, p: Point, deltas: list, search_active: bool = True):
        for d in deltas:
            d1 = p + d
            is_active = self.is_active(d1)
            if search_active and is_active:
                yield d1
            elif not search_active and not is_active:
                yield d1

    def iter_inactive_neighbors_d1(self, p: array):
        yield from self._iter_neightbors(p, self.variations1, search_active=False)

    def iter_inactive_neighbors_d2(self, p: array):
        yield from self._iter_neightbors(p, self.variations2, search_active=False)

    def iter_active_neighbors_d1(self, p: array):
        yield from self._iter_neightbors(p, self.variations1, search_active=True)

    def iter_active_neighbors_d2(self, p: array):
        yield from self._iter_neightbors(p, self.variations2, search_active=True)

    def add_active(self, p):
        dim = 0
        data = self.data
        while dim < (self.ndims - 1):
            i = p[dim]
            if i not in data:
                if dim < (self.ndims - 2):
                    data[i] = {}
                else:
                    data[i] = []
            data = data[i]
            dim += 1

        if p[-1] not in data:
            data.append(p[-1])

    def remove_active(self, p):
        dim = 0
        data = self.data
        while dim < (self.ndims - 1):
            i = p[dim]
            data = data[i]
            dim += 1
        assert isinstance(data, list)
        if p[-1] not in data:
            raise IndexError(f'{p[-1] = } not in {data = }')
        else:
            data.remove(p[-1])


class ConwayCubes:

    def __init__(self, data_p: Union[dict, str], ndims=4):
        self.grid = GridNDCython(str(data_p.abspath()), ndims=ndims)

    def rule2(self):
        """
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
        """
        targets = []
        bad_candidates = set()
        for pa in self.grid.iter_actives():
            neigh_it = self.grid.iter_active_neighbors_d2(pa)
            counter = 0
            for _ in neigh_it:
                if counter >= 1: break
                counter += 1
            if counter >= 1:
                candidates = [c for c in self.grid.iter_inactive_neighbors_d1(pa) if c not in bad_candidates]
                for c in candidates:
                    if len(list(self.grid.iter_active_neighbors_d1(c))) == 3:
                        targets.append(c)
                    else:
                        bad_candidates.add(c)

        return targets

    def rule1(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active,
        the cube remains active. Otherwise, the cube becomes inactive.
        """
        to_set_inactives = []
        for p in self.grid.iter_actives():
            num_actives_around = len(list(self.grid.iter_active_neighbors_d1(p)))
            if not (2 <= num_actives_around <= 3):
                to_set_inactives.append(p)
        return to_set_inactives

    def step(self):
        to_be_rem = self.rule1()
        to_be_add = self.rule2()
        for p in to_be_rem:
            self.grid.remove_active(p)
        for p in to_be_add:
            self.grid.add_active(p)

    def run(self, nsteps: int):
        for i in range(nsteps):
            self.step()
            print('step', i+1, 'done')


if __name__ == '__main__':
    input_path = Path(__file__).parent / 'input.txt'
    c = ConwayCubes(input_path, 4)
    c.run(6)
    print(len(tuple(c.grid.iter_actives())))
