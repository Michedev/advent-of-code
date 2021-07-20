from typing import Tuple, List

from day16.parser import parse


def solve(state):
    matching = is_in_range(state)
    return sum(el[1] for el in matching)


def is_in_range(state) -> List[Tuple[bool, int]]:
    result = []
    for ticket in state.other_tickets:
        result.append(match_any_value(state.fields, ticket))
    return result


def match_any_value(fields, ticket):
    tot_err = 0
    match_any = True
    for value in ticket.values:
        in_range = any(field.range1[0] <= value <= field.range1[1] or
                       field.range2[0] <= value <= field.range2[1] for field in fields)
        if not in_range:
            tot_err += value
            match_any = False
    return match_any, tot_err


def main():
    state = parse('input.txt')
    result = solve(state)
    print(result)


if __name__ == '__main__':
    main()
