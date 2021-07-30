from copy import copy
from ctypes import Union
from itertools import product
from typing import Union

from numpy import array

cdef class Point:
    
    cdef public list c

    def __cinit__(self, c):
        self.c = c

    cdef inline Point __op(self, other, opf):
        if isinstance(other, (int, float)):
            return Point([opf(x, other) for x in self.c])
        return Point([opf(self.c[i], other.c[i]) for i in range(len(self.c))])

    cpdef Point add(self, other):
        if isinstance(other, (int, float)):
            return Point([x + other for x in self.c])
        return Point([(self.c[i] + other.c[i]) for i in range(len(self.c))])

    cpdef Point sub(self, other):
        if isinstance(other, (int, float)):
            return Point([x - other for x in self.c])
        return Point([(self.c[i] - other.c[i]) for i in range(len(self.c))])

    # cpdef Point mul(self, other):
    #     return self.__op(other, lambda a, b: a * b)
    #
    # cpdef Point div(self, other):
    #     return self.__op(other, lambda a, b: a / b)

    def __hash__(self):
        return sum(1000 ** i * self.c[i] for i in range(len(self.c)))

    def __len__(self): return len(self.c)

    def __getitem__(self, item): return self.c[item]

    def __repr__(self): return repr(self.c)

    def __iter__(self): return iter(self.c)


cdef class GridND:

    cdef int ndims
    cdef dict data
    cdef list variations1, variations2

    def __cinit__(self, data_p: Union[dict, str], ndims: int = 3):
        self.ndims = ndims
        if isinstance(data_p, str):
            self.data = self.parse_data(data_p)
        else:
            self.data = data_p
        self.variations1 = [Point(list(d1)) for d1 in product(range(-1, 2), repeat=ndims) if not all(x == 0 for x in d1)]
        self.variations2 = [Point(list(d2)) for d2 in product(range(-2, 3, 2), repeat=ndims) if not all(x == 0 for x in d2)]

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
                        raise ValueError(f'{self.ndims} not supported')
        return data

    cpdef bint is_active(self, Point p):
        data = self.data
        for dim in range(self.ndims - 1):
            i = p[dim]
            if i not in data: return False
            data = data[i]
        return p[-1] in data

    cpdef list iter_actives(self):
        result = []
        if self.ndims == 3:
            for i in self.data:
                for j in self.data[i]:
                    for k in self.data[i][j]:
                        result.append(Point([i, j, k]))
            return result
        elif self.ndims == 4:
            for i in self.data:
                for j in self.data[i]:
                    for k in self.data[i][j]:
                        for l in self.data[i][j][k]:
                            result.append(Point([i, j, k, l]))
            return result
        # dimension variable version doesn't work so i wrote above this explicit version
        acc = []
        for i in self.data:
            acc +=  self.__iter_actives_rec(self.data, i, [i])
        return acc

    cpdef __iter_actives_rec(self, data, i: int, prev):
        if isinstance(data[i], list):
            for x in data[i]:
                return [Point(copy(prev + [x]))]
        acc = []
        for el in data[i]:
            if isinstance(el, list):
                for x in el:
                    return [Point(copy(prev + [x]))]
            else:
                acc += self.__iter_actives_rec(data[i], el, copy(prev + [el]))
        return acc

    def _iter_neightbors(self, p: Point, deltas: list, search_active: bool = True):
        for d in deltas:
            d1 = p.add(d)
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

    def remove_active(self, Point p):
        dim = 0
        data = self.data
        while dim < (self.ndims - 1):
            i = p[dim]
            data = data[i]
            dim += 1
        assert isinstance(data, list)
        if p[-1] not in data:
            raise IndexError(f'{p[-1]} not in {data}')
        else:
            data.remove(p[-1])