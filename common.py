from abc import ABC, abstractmethod

class AOC(ABC):

    @abstractmethod
    def solution1(self):
        pass

    @abstractmethod
    def solution2(self):
        pass

def setup_argparse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=Path)
    parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
    return parser


__all__ = ['AOC', 'setup_argparse']