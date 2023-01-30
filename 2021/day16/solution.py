from dataclasses import dataclass, field
from typing import List, Optional
from template import TemplateSolution
from path import Path
import numpy as np

def bits_str(bits):
    return ''.join([str(int(x)) for x in bits])

@dataclass
class Packet:

    version: int
    type: int
    subpackets: List['Packet'] = field(default_factory=list)
    literal_value: Optional[int] = None

    @property
    def is_literal(self):
        return self.type == 4

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
        'A': [1, 0, 1, 0],
        'B': [1, 0, 1, 1],
        'C': [1, 1, 0, 0],
        'D': [1, 1, 0, 1],
        'E': [1, 1, 1, 0],
        'F': [1, 1, 1, 1],
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
            bits += list(line[i+1:i+5])
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
        if self.verbose:
            print(f'packet_version: {packet_version}, bits: {bits_str(line[:3])}')
            print(f'packet_type: {packet_type}, bits: {bits_str(line[3:6])}')
        if packet_type == 4: # is literal
            if self.verbose:
                print('is literal')
                print('bits: ', bits_str(line[6:]))
            literal, end_index = self.parse_literal(line[6:])
            end_index += 6 # add the 6 bits of the packet header
            result = Packet(packet_version, packet_type, [], literal)
            if self.verbose:
                print(f'literal: {literal}, end_index: {end_index}')
            return result, end_index
        else: # is operator
            # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

            length_type_id = line[6] 
            subpackets_bit_length = 11 if length_type_id == 1 else 15
            subpackets_length = line[7:7+subpackets_bit_length]
            subpackets_length = self.bin_to_dec(subpackets_length)
            subpackets = []
            start_position = 7+subpackets_bit_length
            if self.verbose:
                print(f'length_type_id: {int(length_type_id)}')
            if length_type_id:
                num_subpackets = subpackets_length
                return self.subpacket_bit_length_1(line, subpackets_bit_length, subpackets, start_position, num_subpackets, packet_version, packet_type)
            else:
                return self.subpacket_bit_length_0(line, packet_version, packet_type, subpackets_length, start_position)

    def subpacket_bit_length_1(self, line, subpackets_bit_length, subpackets, start_position, num_subpackets, packet_version, packet_type):
        if self.verbose:
            print(f'num_subpackets: {num_subpackets}', 'bits: ', bits_str(line[7:7+subpackets_bit_length]))
        for i in range(num_subpackets):
            if self.verbose:
                print('=' * 50)
                print('subsequence:', "".join([str(int(x)) for x in line[start_position:]]))
                print('subpacket:', i+1, 'of', num_subpackets)
                print('=' * 50)

            subpacket, end_position = self.calc_line(line[start_position:])
            if self.verbose:
                print(f'subpackets value: {subpacket}, end_position: {end_position}')
            start_position += end_position 
            subpackets.append(subpacket)
        return Packet(packet_version, packet_type, subpackets), start_position


    def subpacket_bit_length_0(self, line, packet_version, packet_type, subpackets_length, start_position):
        if self.verbose:
            print(f'subpackets_length: {subpackets_length}')
        subpackages = []
        subsequence = line[start_position:start_position+subpackets_length]
        if self.verbose:
            print('=' * 50)
            print('subsequence:', "".join([str(int(x)) for x in subsequence]))
            print('=' * 50)
        subpacket, pos = self.calc_line(subsequence)
        subpackages.append(subpacket)
        start_position = pos
        i = 2
        while start_position < subpackets_length :
            if self.verbose:
                print('=' * 30)
                print(f'subsequence #{i}:', bits_str(subsequence[start_position:]))
                print('=' * 30)
            subpacket, pos = self.calc_line(subsequence[start_position:])
            start_position += pos
            subpackages.append(subpacket)
            i += 1
        result = Packet(packet_version, packet_type, subpackages)
        if self.verbose:
            print(f'subpackets value: {subpacket}, end_position: {pos}')
        return result, subpackets_length + start_position

    def sum_version(self, packet: Packet):
        result = packet.version
        for subpacket in packet.subpackets:
            result += self.sum_version(subpacket)
        return result
    
    def solution1(self, data: List[np.array]):
        packets = []

        for i, line in enumerate(data):
            if self.verbose:
                print(f'line number {i}')
                print(f'line: {"".join([str(int(x)) for x in line])}')
            result, pos = self.calc_line(line)
            packets.append(result)
            if self.verbose:
                print('total:', self.sum_version(result))
                print('*' * 50)
        total = 0
        for packet in packets:
            packet_version_sum = self.sum_version(packet)
            total += packet_version_sum
            if self.verbose:
                print(f'packet_version_sum: {packet_version_sum}')
        return total
    
    
    def solution2(self, data):
        pass


if __name__ == '__main__':
    Solution().main()