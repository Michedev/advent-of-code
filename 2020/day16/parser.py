import re
from dataclasses import dataclass
from typing import List


@dataclass
class Field:
    name: str
    range1: List[int]
    range2: List[int]

    def in_any_range(self, value: int):
        return (self.range1[0] <= value <= self.range1[1]) or (self.range2[0] <= value <= self.range2[1])

@dataclass
class Ticket:
    values: List[int]

@dataclass
class State:
    fields: List[Field]
    my_ticket: Ticket
    other_tickets: List[Ticket]


def parse_fields(text):
    result = []
    parser = re.compile(r'(?P<name>[\w,\s]+): (?P<range1>[\d,-]+) or (?P<range2>[\d,-]+)')
    for line in text.split('\n'):
        if g := parser.match(line):
            name = g.group('name')
            range1 = g.group('range1').split('-')
            range2 = g.group('range2').split('-')
            range1 = [int(x) for x in range1]
            range2 = [int(x) for x in range2]
            result.append(Field(name, range1, range2))
    return result


def parse_my_ticket(text):
    ticker_line = False
    for line in text.split('\n'):
        if ticker_line:
            ticket_values = [int(x) for x in line.split(',')]
            return Ticket(ticket_values)
        if line == 'your ticket:':
            ticker_line = True


def parse_other_tickets(text):
    other_tickets = []
    other_tickets_line = False
    for line in text.split('\n'):
        if other_tickets_line:
            ticket_values = [int(x) for x in line.split(',')]
            assert len(ticket_values) > 2
            other_tickets.append(Ticket(ticket_values))
        if line == 'nearby tickets:':
            other_tickets_line = True
    return other_tickets


def parse(fname='input.txt'):
    with open(fname, 'r') as f:
        text = f.read()
        return State(parse_fields(text), parse_my_ticket(text), parse_other_tickets(text))