import re
from dataclasses import dataclass
from path import Path
from numpy import array, squeeze, expand_dims
from typing import Union




class BoatMover:

    def __init__(self, actions: Union[list, str], start_pos = (0, 0), direction = 'E', waypoint_pos = None):
        self.actions = actions
        if isinstance(actions, str):
            self.actions = self.parse_actions(actions)
        if isinstance(start_pos, (list, tuple)): start_pos = array(start_pos)
        self.start_pos = start_pos
        self.pos = start_pos
        self.direction = direction.upper()
        self.cardinal_move = re.compile(r'(?P<direction>[NSWEF])(?P<module>[0-9]+)')
        self.rotation_move = re.compile(r'(?P<direction>L|R)(?P<angle>[0-9]+)')
        if waypoint_pos is not None: waypoint_pos = array(waypoint_pos)
        self.waypoint_pos = waypoint_pos
        self.right_directions = ['E', 'S', 'W', 'N']
        self.direction_signs = {'E': array((0, 1)), 'W': array((0, -1)), 'N': array((1, 0)), 'S': array((-1, 0))}
        self.direction_rotations = {'N': None, 'S': ('L', 180), 'W': ('L', 90), 'E': ('R', 90)}
        self.left_directions = list(reversed(self.right_directions))

    def parse_actions(self, path_actions: str):
        with open(path_actions) as f:
            return [a for a in f.read().split('\n') if a]

    def move_(self, direction, module):
        self.pos = self._move(self.pos, direction, module)

    def _move(self, p0, direction, module):
        if direction == 'F': direction = self.direction
        sign = self.direction_signs[direction]
        vector = sign * module
        return p0 + vector

    def move_by_waypoint_(self, direction, module):
        if direction == 'F':
            self.pos = self.pos + self.waypoint_pos * module
        else:
            self.waypoint_pos = self._move(self.waypoint_pos, direction, module) 

    def rotate(self, boat_way, angle):
        directions = self.left_directions if boat_way == 'L' else self.right_directions
        curr_i = directions.index(self.direction)
        new_i = (curr_i + (angle // 90)) % len(directions)
        new_direction = directions[new_i]
        return new_direction

    def rotate_(self, boat_way, angle):
        new = self.rotate(boat_way, angle)
        self.direction = new

    def rotate_waypoint(self, boat_way, angle):
        """
        >>> mb = BoatMover([], waypoint_pos = (4, 10))
        >>> tuple(mb.rotate_waypoint('L', 90))
        (10, -4)
        >>> tuple(mb.rotate_waypoint('L', 180))
        (-4, -10)
        >>> tuple(mb.rotate_waypoint('R', 90))
        (-10, 4)
        >>> tuple(mb.rotate_waypoint('R', 180))
        (-4, -10)
        >>> (mb.rotate_waypoint('R', 270) == mb.rotate_waypoint('L', 90)).all()
        True
        >>> (mb.rotate_waypoint('R', 90) == mb.rotate_waypoint('L', 270)).all()
        True
        >>> (mb.rotate_waypoint('R', 180) == mb.rotate_waypoint('L', 180)).all()
        True
        """

        if boat_way == 'R':
            rotation_matrix = array([[0, 1], [-1, 0]])
        else:
            rotation_matrix = array([[0, -1], [1, 0]])
        new_waypoint = expand_dims(array(self.waypoint_pos), axis=0)
        for _ in range(angle//90):
            new_waypoint = new_waypoint @ rotation_matrix
        new_waypoint = squeeze(new_waypoint, axis=0)
        return new_waypoint

    def rotate_waypoint_(self, boat_way, angle):
        new_w = self.rotate_waypoint(boat_way, angle)
        self.waypoint_pos = new_w

    def step_(self, action):
        if (m := self.cardinal_move.fullmatch(action)) is not None:
            d, i = m.group('direction'), int(m.group('module'))
            self.move_(d, i)
        elif (m := self.rotation_move.fullmatch(action)) is not None:
            direction, angle = m.group('direction'), int(m.group('angle'))
            self.rotate_(direction, angle)
        else:
            raise ValueError(f'"{action}" not correctly parsed')

    def step2_(self, action):
        if (m := self.cardinal_move.fullmatch(action)) is not None:
            d, i = m.group('direction'), int(m.group('module'))
            self.move_by_waypoint_(d, i)
        elif (m := self.rotation_move.fullmatch(action)) is not None:
            direction, angle = m.group('direction'), int(m.group('angle'))
            self.rotate_waypoint_(direction, angle)
        else:
            raise ValueError(f'"{action}" not correctly parsed')


    def solution1(self):
        for action in self.actions:
            self.step_(action)
        return abs(bm.pos).sum()


    def solution2(self):
        for action in self.actions:
            self.step2_(action)
        return abs(bm.pos).sum()

    @classmethod
    def setup_solution2(cls, input_path: str):
        return cls(input_path, start_pos=(0, 0), waypoint_pos=(1, 10) )


if __name__ == "__main__":
    example_path = Path(__file__).parent / 'input.txt'
    bm = BoatMover.setup_solution2(example_path)
    print(bm.solution2())
    print(bm.pos, bm.direction)
    print(abs(bm.pos).sum()) # 31164 too low