from path import Path
from template import TemplateSolution
import re

# If any regular number is 10 or greater, the leftmost such regular number splits.
regex_split = re.compile(r'(\d{2,})')

# If any pair is nested inside four pairs, the leftmost such pair explodes.
regex_explode = re.compile(
    r'\[.*\[.*\[.*(?P<target>\[(?P<a>\d+),(?P<b>\d+)\])')


def find_before_after_numbers(data, match: re.Match):
    i_start = match.start('target')
    i_start_len = 1
    i_end = match.end('target')
    i_end_len = 1
    while i_start >= 0:
        i_start -= 1
        if data[i_start].isnumeric():
            break
    if i_start > 0 and data[i_start - 1].isnumeric():
        i_start -= 1
        i_start_len += 1
    while i_end < len(data):
        i_end += 1
        if i_end < len(data) and data[i_end].isnumeric():
            break
    if i_end < len(data) - 1 and data[i_end + 1].isnumeric():
        i_end_len += 1
    return i_start, i_start_len, i_end, i_end_len


def explode(data):
    """

    >>> explode('[2,3]')
    '[2,3]'
    >>> explode('[[[2,[2,3],4]]]')
    '[[[4,7]]]'
    >>> explode('[[9,[2,[3,3],4]]]')
    '[[9,[5,7]]]'
    >>> explode('[[9,[2,[13,3],4],3]]')
    '[[9,[15,7],3]]'

    """
    try:
        match = next(iter(regex_explode.finditer(data)))
    except StopIteration:
        return data
    if match:
        a, b = int(match.group('a')), int(match.group('b'))
        i_before, before_len, i_after, after_len = find_before_after_numbers(
            data, match)
        if i_before >= 0 and i_after < len(data):
            data = data[:i_before] + str(int(data[i_before:i_before + before_len]) + a) + data[i_before +
                                                                                               before_len:i_after] + str(int(data[i_after:i_after + after_len]) + b) + data[i_after+after_len:]
        elif i_after < len(data):
            data = data[:i_after] + \
                str(int(data[i_after:i_after + after_len]) + b) + \
                data[i_after+after_len:]
        elif i_before > 0:
            data = data[:i_before] + str(
                int(data[i_before:i_before + before_len]) + a) + data[i_before+before_len:]
        else:
            pass

        i_start = match.start('target')
        i_end = match.end('target')
        data = data[:i_start] + data[i_end+1:]

    return data


def split(data):
    """
    To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    >>> split('[1,4]')
    '[1,4]'
    >>> split('[1,15]')
    '[1,[7,8]]'
    >>> split('[1,[7,18]]')
    '[1,[7,[9,9]]]'
    >>> split('[1,[7,[9,20]]]')
    '[1,[7,[9,[10,10]]]]'
    """

    try:
        match = next(iter(regex_split.finditer(data)))
    except StopIteration:
        return data
    if match:
        i_start = match.start()
        i_end = match.end()
        a = int(data[i_start:i_end])
        data = data[:i_start] + f'[{a//2},{a//2 + a % 2}]' + data[i_end:]
    return data

class Solution(TemplateSolution, day=18, year=2021):

    def data_path(self):
        return Path(__file__).parent

    def parse(self, input_file: Path):
        return input_file.read_text().splitlines()
