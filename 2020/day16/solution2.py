from copy import copy
from random import shuffle

from day16.parser import parse
from day16.solution1 import is_in_range


def find_fields_assignment(state):
    is_correct = is_in_range(state)
    good_tickets = [el for i, el in enumerate(state.other_tickets) if is_correct[i][0]] + [state.my_ticket]
    field_indexes = []
    found_fields = []
    print(good_tickets)
    remaining_indexes = list(range(len(state.fields)))
    while len(field_indexes) < len(state.fields):
        for field in state.fields:
            if field not in found_fields:
                field_index = get_field_index(field, good_tickets, remaining_indexes)
                if field_index is None:
                    print('Value for field', field.name, 'not found')
                else:
                    print('field:', field.name, '=', field_index)
                    field_indexes.append(field_index)
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


def find_possible_index(field, good_tickets, remaining_indexes):
    possible_indexes = copy(remaining_indexes)
    for ticket in good_tickets:
        for i, value in enumerate(ticket.values):
            if i in possible_indexes:
                match_field = field.in_any_range(value)
                if not match_field:
                    possible_indexes.remove(i)
            if len(possible_indexes) == 1:
                return possible_indexes[0]


def solve(state):
    field_index = find_fields_assignment(state)
    result = 1
    shuffle(state.fields)
    for field, field_index in zip(state.fields, field_index):
        if field.name.startswith('departure '):
            print(field.name, f'[{field_index}]', ':', state.my_ticket.values[field_index])
            result *= state.my_ticket.values[field_index]
    return result


def main():
    state = parse('input.txt')
    result = solve(state)
    assert result > 503022490723, 'result is too low (output website)'
    assert result > 612440092903, 'result is too low (output website)'
    print(result)


if __name__ == '__main__':
    main()
