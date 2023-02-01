from dataclasses import dataclass, field
from math import prod
from typing import Iterable, List, Optional, Tuple
from template import TemplateSolution
from path import Path
import numpy as np
import logging

def bits_str(bits):
    return ''.join([str(int(x)) for x in bits])

@dataclass
class Packet:

    version: int
    type: int
    subpackets: List['Packet'] = field(default_factory=list)
    literal_value: Optional[int] = None
    start_index: Optional[int] = None
    end_index: Optional[int] = None

    @property
    def is_literal(self):
        return self.type == 4

    def solve(self, verbose=False):
        """
        Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0 These packets always have exactly two sub-packets.
        """
        if self.is_literal:
            if verbose:
                print(f'Literal: {self.literal_value}')
            return self.literal_value
        if self.type == 0:
            if verbose:
                print(f'Sum operator')
            return sum([p.solve(verbose) for p in self.subpackets])
        if self.type == 1:
            if verbose:
                print(f'Prod operator')
            return prod([p.solve(verbose) for p in self.subpackets])
        if self.type == 2:
            if verbose:
                print(f'Min operator')
            return min([p.solve(verbose) for p in self.subpackets])
        if self.type == 3:
            if verbose:
                print(f'Max operator')
            return max([p.solve(verbose) for p in self.subpackets])
        if self.type == 5:
            if verbose:
                print(f'Greater than operator')
            return int(self.subpackets[0].solve(verbose) > self.subpackets[1].solve(verbose))
        if self.type == 6:
            if verbose:
                print(f'Less than operator')
            return int(self.subpackets[0].solve(verbose) < self.subpackets[1].solve(verbose))
        if self.type == 7:
            if verbose:
                print(f'Equal to operator')
            return int(self.subpackets[0].solve(verbose) == self.subpackets[1].solve(verbose))
        raise ValueError(f'Unknown type {self.type}')

def encode_bits(bits: Iterable[int]) -> str:
    result = ''
    for i in range(0, len(bits), 4):
        result += Solution.dict_hex_inversed[tuple(bits[i:i+4])]
    return result

class Solution(TemplateSolution, year=2021, day=16):

    dict_hex = {
        '0': (0, 0, 0, 0),
        '1': (0, 0, 0, 1),
        '2': (0, 0, 1, 0),
        '3': (0, 0, 1, 1),
        '4': (0, 1, 0, 0),
        '5': (0, 1, 0, 1),
        '6': (0, 1, 1, 0),
        '7': (0, 1, 1, 1),
        '8': (1, 0, 0, 0),
        '9': (1, 0, 0, 1),
        'A': (1, 0, 1, 0),
        'B': (1, 0, 1, 1),
        'C': (1, 1, 0, 0),
        'D': (1, 1, 0, 1),
        'E': (1, 1, 1, 0),
        'F': (1, 1, 1, 1),
    }

    dict_hex_inversed = {tuple(v): k for k, v in dict_hex.items()}

    
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
        literal_value = 0
        bits = []
        for i in range(0, len(line), 5):
            bits += list(line[i+1:i+5])
            if line[i] == 0:
                break
        literal_value = self.bin_to_dec(bits)
        ending_index = i+5
        return literal_value, ending_index

    
    
    def parse_packet(self, bits: np.array, start_index: int) -> Tuple[Packet, int]:
        packet_version = bits[0:3]
        packet_version = self.bin_to_dec(packet_version)
        packet_type = bits[3:6]
        packet_type = self.bin_to_dec(packet_type)
        if self.verbose:
            print(f'packet_version: {packet_version}, bits: {bits_str(bits[:3])}')
            print(f'packet_type: {packet_type}, bits: {bits_str(bits[3:6])}')
        if packet_type == 4: # is literal
            if self.verbose:
                print('is literal')
                print('bits: ', bits_str(bits[6:]))
            literal, literal_length = self.parse_literal(bits[6:])
            literal_length += 6 # add the 6 bits of the packet header
            result = Packet(packet_version, packet_type, [], literal, start_index=start_index, end_index=start_index + literal_length)
            if self.verbose:
                print(f'literal: {literal}, end_index: {literal_length}')
            return result, literal_length
        else: # is operator
            # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

            length_type_id = bits[6] 
            subpackets_field_length = 11 if length_type_id == 1 else 15
            subpackets_field = bits[7:7+subpackets_field_length]
            subpackets_field = self.bin_to_dec(subpackets_field)
            start_position = 7+subpackets_field_length
            if self.verbose:
                print(f'length_type_id: {int(length_type_id)}')
            if length_type_id:
                num_subpackets = subpackets_field
                return self.subpacket_bit_length_1(bits, start_index, subpackets_field_length, num_subpackets, packet_version, packet_type)
            else:
                return self.subpacket_bit_length_0(bits, start_index, packet_version, packet_type, subpackets_field)

    def subpacket_bit_length_1(self, line: np.array, start_index: int,  subpackets_bit_length: int,  num_subpackets: int, packet_version: int, packet_type: int):
        start_position = 7 + 11
        subpackets = []
        if self.verbose:
            print(f'num_subpackets: {num_subpackets}', 'bits: ', bits_str(line[7:7+subpackets_bit_length]))
        for i in range(num_subpackets):
            if self.verbose:
                print('=' * 50)
                print('subsequence:', "".join([str(int(x)) for x in line[start_position:]]))
                print('subpacket:', i+1, 'of', num_subpackets)
                print('=' * 50)

            subpacket, end_position = self.parse_packet(line[start_position:], start_index + start_position)
            if self.verbose:
                print(f'subpackets value: {subpacket}, end_position: {end_position}')
            start_position += end_position
            subpackets.append(subpacket)
        end_position = start_position # rename for clarity
        return Packet(packet_version, packet_type, subpackets, start_index=start_index, end_index=start_index + end_position), end_position


    def subpacket_bit_length_0(self, line: np.array, start_index: int, packet_version: int, packet_type: int, subpackets_length: int):
        start_position = 7 + 15
        expected_end_pos = start_position + subpackets_length
        if self.verbose:
            print(f'subpackets_length: {subpackets_length}')
        subpackets = []
        subsequence = line[start_position:start_position+subpackets_length]
        if self.verbose:
            print('=' * 50)
            print('subsequence:', "".join([str(int(x)) for x in subsequence]))
            print('=' * 50)
        subpacket, pos = self.parse_packet(subsequence, start_index + start_position)
        subpackets.append(subpacket)
        start_position += pos
        i = 2
        if self.verbose:
            print('start_position:', start_position)
            print('subpackets_length:', subpackets_length)
        while (expected_end_pos - start_position) > 6 : # 6 is the length of the packet header
            if self.verbose:
                print('=' * 30)
                print(f'subsequence #{i}:', bits_str(line[start_position:]))
                print('=' * 30)
            subsequence = line[start_position:start_position+subpackets_length]
            subpacket, pos = self.parse_packet(subsequence, start_index + start_position)
            start_position += pos
            subpackets.append(subpacket)
            i += 1
            if self.verbose:
                print('start_position:', start_position)
                print('subpackets_length:', subpackets_length)

        end_position = start_position # rename for clarity
        result = Packet(packet_version, packet_type, subpackets, start_index=start_index, end_index=start_index + end_position)
        if self.verbose:
            print(f'subpackets value: {subpacket}, end_position: {end_position}')
        return result, end_position

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
            result, pos = self.parse_packet(line, 0)
            packets.append(result)
            if self.verbose:
                print('total:', self.sum_version(result))
                print('*' * 50)
        total = 0
        for i, packet in enumerate(packets):
            packet_version_sum = self.sum_version(packet)
            total += packet_version_sum
            if self.verbose:
                print(f'packet_version_sum: {packet_version_sum}')
                print(bits_str(data[i]))
                self.print_occupied_bits(packet, len(data[i]))
        return total
    
    def print_occupied_bits(self, packet: Packet, bits_length: int, occupied_chr: str = 'A'):
        occupied = [' ' for _ in range(bits_length) ]
        for i in range(bits_length):
            if packet.start_index <= i <= packet.end_index:
                occupied[i] = occupied_chr
        print("".join(occupied))
        for subpacket in packet.subpackets:
            occupied = self.print_occupied_bits(subpacket, bits_length, chr(ord(occupied_chr) + 1))
        
    def solution2(self, data):
        packets = []

        for i, line in enumerate(data):
            if self.verbose:
                print(f'line number {i}')
                print(f'line: {"".join([str(int(x)) for x in line])}')
            result, pos = self.parse_packet(line, 0)
            packets.append(result)
            if self.verbose:
                print('total:', self.sum_version(result))
                print('*' * 50)
        result = []
        for packet in packets:
            packet_value = packet.solve(self.verbose)
            if self.verbose:
                print(f'packet_value: {packet_value}')
            result.append(packet_value)
        if len(result) == 1:
            return result[0]
        return result

if __name__ == '__main__':
    Solution().main()