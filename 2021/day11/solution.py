import argparse
from path import Path
import numpy as np

from template import TemplateSolution


class SolutionDay11(TemplateSolution):

    
    def data_path(self):
        return Path(__file__).parent

    
    def parse(self, input_file):
        """
        >>> data = SolutionDay11.parse_2dmatrix_single_digit('input_test.txt')
        >>> np.all(data == np.array([[1,2],[3,4]]))
        True
        """
        with open(input_file) as f:
            data = f.read().split('\n')
        data = [[int(x) for x in row] for row in data]
        return np.array(data)

    
    def step(self, data):
        data += 1
        data, num_flashes = self.flashes_phase(data)
        data = data * (~ self.will_flash(data)).astype('int')
        return data, num_flashes

    
    def solution1(self, data):
        tot = 0
        for _ in range(100):
            data, num_flashes = self.step(data)
            tot += num_flashes
        return tot

    
    def solution2(self, data):
        all_flashes = False
        step = 0
        num_el = data.shape[0] * data.shape[1]
        while not all_flashes:
            data, num_flashes = self.step(data)
            all_flashes = num_el == num_flashes
            step += 1
        return step

    
    def flashes_phase(self, data):
        num_flashes = 0
        has_been_flashed = np.zeros_like(data, dtype=bool)
        to_flash = self.will_flash(data)
        effective_to_flash = to_flash & (~ has_been_flashed)
        while np.any(effective_to_flash):
            num_flashes += np.sum(effective_to_flash)
            for i in range(effective_to_flash.shape[0]):
                for j in range(effective_to_flash.shape[1]):
                    if effective_to_flash[i, j]:
                        neighbors = self.get_neighbors_2d_matrix(effective_to_flash, i, j)
                        for _, i0, j0 in neighbors:
                            data[i0, j0] = data[i0, j0] + 1
            has_been_flashed = has_been_flashed | to_flash
            to_flash = self.will_flash(data)
            effective_to_flash = to_flash & (~ has_been_flashed)
        return data, num_flashes

    
    def will_flash(self, data):
        return data > 9


def test_step():
    data = np.array([[1] * 5, [1, 9, 9, 9, 1], [1, 9, 1, 9, 1], [1, 9, 9, 9, 1], [1, 1, 1, 1, 1]])
    exp_output = np.array([[3, 4, 5, 4, 3], [4, 0, 0, 0, 4], [5, 0, 0, 0, 5], [4, 0, 0, 0, 4], [3, 4, 5, 4, 3]])
    output, num_flashes = SolutionDay11.step(data)
    equals = np.all(exp_output == output)
    assert equals, output


if __name__ == '__main__':
    SolutionDay11.main()
