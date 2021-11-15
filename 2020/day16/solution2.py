from copy import copy
from random import shuffle
from path import Path

from parser import parse
from solution1 import is_in_range


def find_fields_assignment(state):
    is_correct = is_in_range(state)
    good_tickets = [el for i, el in enumerate(state.other_tickets) if is_correct[i][0]] + [state.my_ticket]
    field_indexes = []
    found_fields = []
    remaining_indexes = list(range(len(state.fields)))
    while len(field_indexes) < len(state.fields):
        for field in state.fields:
            if field not in found_fields:
                field_index = get_field_index(field, good_tickets, remaining_indexes)
                if field_index is None:
                    print('Value for field', field.name, 'not found')
                else:
                    print('field:', field.name, '=', field_index)
                    field_indexes.append((field_index, field))
                    remaining_indexes.remove(field_index)
                    found_fields.append(field)
    return field_indexes


def validate_field(field, field_index, tickets):
    for ticket in tickets:
        if not field.in_any_range(ticket.values[field_index]):
            return None
    return field_index


def get_field_index(field, tickets, remaining_indexes):
    field_index = find_possible_index(field, tickets, remaining_indexes)
    if field_index is not None:
        return validate_field(field, field_index, tickets)
    return None


def find_possible_index(field, tickets, remaining_indexes):
    possible_indexes = copy(remaining_indexes)
    for i in remaining_indexes:
        for ticket in tickets:
                match_field = ticket.values[i] in field
                if not match_field:
                    possible_indexes.remove(i)
                    break
    if len(possible_indexes) == 1:
        return possible_indexes[0]


def solve(state):
    field_indexes = find_fields_assignment(state)
    result = 1
    shuffle(state.fields)
    for field_index, field in field_indexes:
        if field.name.startswith('departure '):
            print(field.name, f'[{field_index}]', ':', state.my_ticket.values[field_index])
            result *= state.my_ticket.values[field_index]
    return result


def main():
    input_path = Path(__file__).parent / 'input.txt'
    state = parse(input_path)
    result = solve(state)
    assert result > 503022490723, 'result is too low (output website)'
    assert result > 612440092903, 'result is too low (output website)'
    print(result)


if __name__ == '__main__':
    main()
