from typing import List
from template import TemplateSolution
from path import Path
import numpy as np

class Solution(TemplateSolution, year=2021, day=16):

    dict_hex = {
        '0': [0, 0, 0, 0],
        '1': [0, 0, 0, 1],
        '2': [0, 0, 1, 0],
        '3': [0, 0, 1, 1],
        '4': [0, 1, 0, 0],
        '5': [0, 1, 0, 1],
        '6': [0, 1, 1, 0],
        '7': [0, 1, 1, 1],
        '8': [1, 0, 0, 0],
        '9': [1, 0, 0, 1],
        'a': [1, 0, 1, 0],
        'b': [1, 0, 1, 1],
        'c': [1, 1, 0, 0],
        'd': [1, 1, 0, 1],
        'e': [1, 1, 1, 0],
        'f': [1, 1, 1, 1],
    }

    
    def data_path(self):
        return Path(__file__).parent

    
    def parse(self, input_file) -> List[np.array]:
        result = []
        with open(input_file) as f:
            data = f.read().split('\n')
        for line in data:
            bit_line = np.zeros(len(line) * 4, dtype=bool)
            for i, c in enumerate(line):
                bit_line[i*4:(i+1)*4] = self.dict_hex[c]
            result.append(bit_line)
        return result
    
    
    def bin_to_dec(self, line: np.array):
        result = 0
        for i in range(len(line)):
            result += line[i] * 2 ** (len(line) - i - 1)
        return result

    
    def parse_literal(self, line: np.array):
        """
        Literal value packets encode a single binary number. To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed by a 0 bit. 
        """
        result = 0
        bits = []
        for i in range(0, len(line), 5):
            bits += line[i+1:i+5]
            if line[i] == 0:
                break
        result = self.bin_to_dec(bits)
        ending_index = i+5
        return result, ending_index
    
    def calc_line(self, line: np.array):
        packet_version = line[0:3]
        packet_version = self.bin_to_dec(packet_version)
        packet_type = line[3:6]
        packet_type = self.bin_to_dec(packet_type)
        if packet_type == 4: # is literal
            literal, end_index = self.parse_literal(line[6:])
            return literal, end_index
        else: # is operator
            # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

            length_type_id = line[6] 
            subpackets_length = 11 if length_type_id == 0 else 15
            subpackets_length = line[7:7+subpackets_length]
            subpackets_length = self.bin_to_dec(subpackets_length)
            subpackets = []
            start_position = 7+subpackets_length
            if length_type_id:
                num_subpackets = subpackets_length
                for _ in range(num_subpackets):
                    value, end_position = self.calc_line(line[start_position:])
                    start_position += end_position
                    subpackets.append(value)
                return sum(subpackets), start_position
            else:
                subpackets = line[start_position:start_position+subpackets_length]
                value, pos = self.calc_line(subpackets)
                return value, pos + start_position

    
    def solution1(self, data: List[np.array]):
        total = 0
        for line in data:
            total += self.calc_line(line)
        return total
    
    
    def solution2(self, data):
        pass


if __name__ == '__main__':
    Solution().main()