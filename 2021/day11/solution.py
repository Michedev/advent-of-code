import argparse
from path import Path
import numpy as np

from template import TemplateSolution


class SolutionDay11(TemplateSolution):

    @classmethod
    def data_path(cls):
        return Path(__file__).parent

    @classmethod
    def parse(cls, input_file):
        """
        >>> data = SolutionDay11.parse_2dmatrix_single_digit('input_test.txt')
        >>> np.all(data == np.array([[1,2],[3,4]]))
        True
        """
        with open(input_file) as f:
            data = f.read().split('\n')
        data = [[int(x) for x in row] for row in data]
        return np.array(data)

    @classmethod
    def step(cls, data):
        data += 1
        data, num_flashes = cls.flashes_phase(data)
        data = data * (~ cls.will_flash(data)).astype('int')
        return data, num_flashes

    @classmethod
    def solution1(cls, data):
        tot = 0
        for _ in range(100):
            data, num_flashes = cls.step(data)
            tot += num_flashes
        return tot

    @classmethod
    def solution2(cls, data):
        all_flashes = False
        step = 0
        num_el = data.shape[0] * data.shape[1]
        while not all_flashes:
            data, num_flashes = cls.step(data)
            all_flashes = num_el == num_flashes
            step += 1
        return step

    @classmethod
    def flashes_phase(cls, data):
        num_flashes = 0
        has_been_flashed = np.zeros_like(data, dtype=bool)
        to_flash = cls.will_flash(data)
        effective_to_flash = to_flash & (~ has_been_flashed)
        while np.any(effective_to_flash):
            num_flashes += np.sum(effective_to_flash)
            for i in range(effective_to_flash.shape[0]):
                for j in range(effective_to_flash.shape[1]):
                    if effective_to_flash[i, j]:
                        neighbors = cls.get_neighbors_2d_matrix(effective_to_flash, i, j)
                        for _, i0, j0 in neighbors:
                            data[i0, j0] = data[i0, j0] + 1
            has_been_flashed = has_been_flashed | to_flash
            to_flash = cls.will_flash(data)
            effective_to_flash = to_flash & (~ has_been_flashed)
        return data, num_flashes

    @classmethod
    def will_flash(cls, data):
        return data > 9


def test_step():
    data = np.array([[1] * 5, [1, 9, 9, 9, 1], [1, 9, 1, 9, 1], [1, 9, 9, 9, 1], [1, 1, 1, 1, 1]])
    exp_output = np.array([[3, 4, 5, 4, 3], [4, 0, 0, 0, 4], [5, 0, 0, 0, 5], [4, 0, 0, 0, 4], [3, 4, 5, 4, 3]])
    output, num_flashes = SolutionDay11.step(data)
    equals = np.all(exp_output == output)
    assert equals, output


if __name__ == '__main__':
    SolutionDay11.main()
