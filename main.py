# Sodoku Solver

from typing import Optional

Tile = Optional[int]

GameState = list[Tile]


game_state = []
columns = []
rows = []
regions = []


def deserialize_game_state(input: str) -> GameState:
    state = []
    for line in input.splitlines():
        for c in line:
            if c == " " or c == ".":
                state.append(None)
            else:
                state.append(int(c))

    return state


def serialize_game_state(state: GameState) -> str:
    lines = []
    for line_start in range(0, 81, 9):
        line = state[line_start : line_start + 9]
        lines.append("".join(str(n) if n is not None else "." for n in line))

    return "\n".join(lines)


def get_columns(state: GameState) -> list[list[Tile]]:
    columns = []
    for column in range(9):
        column_indices = range(column, 81, 9)
        columns.append([state[i] for i in column_indices])

    return columns


def get_rows(state: GameState) -> list[list[Tile]]:
    rows = []
    for row in range(0, 81, 9):
        row_indices = range(row, row + 9)
        rows.append([state[i] for i in row_indices])

    return rows


def get_regions(state: GameState) -> list[list[Tile]]:
    regions = []
    for region_row in range(0, 9, 3):
        for region_column in range(0, 9, 3):
            region_start = 9 * region_row + region_column
            region_indices = [
                *list(range(region_start + 0, region_start + 3 + 0)),
                *list(range(region_start + 9, region_start + 3 + 9)),
                *list(range(region_start + 18, region_start + 3 + 18)),
            ]
            regions.append([state[i] for i in region_indices])

    return regions


def is_game_over(state: GameState) -> bool:
    correct = [list(range(1, 10))] * 9

    def sorted_if_not_none(input: list[Tile]):
        is_not_null = lambda x: x is not None
        if all(map(is_not_null, input)):
            return sorted(input)
        else:
            return input

    def prep(input: list[list[Tile]]):
        return list(map(sorted_if_not_none, input))

    fs = [get_columns, get_rows, get_regions]
    return all(prep(f(state)) == correct for f in fs)


def is_game_valid(state: GameState) -> bool:
    for x in [*get_columns(state), *get_rows(state), *get_regions(state)]:
        if not is_valid(x):
            return False

    return True


def is_valid(tiles: list[Tile]) -> bool:
    if len(tiles) != 9:
        return False

    counter = {}
    for tile in (t for t in tiles if t is not None):
        count = counter.get(tile, None)
        if count is not None:
            return False
        counter[tile] = 1

    return True


def solve(state: GameState) -> GameState:
    print(serialize_game_state(state))

    def set_state(state: GameState, index: int, value: Tile) -> GameState:
        new_state = state.copy()
        new_state[index] = value
        return new_state

    if is_game_over(state):
        return state

    i = [index for index, val in enumerate(state) if val is None][0]

    valid_states = filter(is_game_valid, (set_state(state, i, s) for s in range(1, 10)))
    try:
        return next(filter(lambda x: x is not None, map(solve, valid_states)))
    except StopIteration as s:
        return None


import pytest


def test_game_state_io():
    game_as_text = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    game_as_data = [
        5,
        3,
        None,
        None,
        7,
        None,
        None,
        None,
        None,
        6,
        None,
        None,
        1,
        9,
        5,
        None,
        None,
        None,
        None,
        9,
        8,
        None,
        None,
        None,
        None,
        6,
        None,
        8,
        None,
        None,
        None,
        6,
        None,
        None,
        None,
        3,
        4,
        None,
        None,
        8,
        None,
        3,
        None,
        None,
        1,
        7,
        None,
        None,
        None,
        2,
        None,
        None,
        None,
        6,
        None,
        6,
        None,
        None,
        None,
        None,
        2,
        8,
        None,
        None,
        None,
        None,
        4,
        1,
        9,
        None,
        None,
        5,
        None,
        None,
        None,
        None,
        8,
        None,
        None,
        7,
        9,
    ]
    game_state = deserialize_game_state(game_as_text)
    assert len(game_state) == len(game_as_data)
    assert game_state == game_as_data
    assert serialize_game_state(game_state) == game_as_text


def test_get_columns():
    game_as_text = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    expected = [
        [5, 6, None, 8, 4, 7, None, None, None],
        [3, None, 9, None, None, None, 6, None, None],
        [None, None, 8, None, None, None, None, None, None],
        [None, 1, None, None, 8, None, None, 4, None],
        [7, 9, None, 6, None, 2, None, 1, 8],
        [None, 5, None, None, 3, None, None, 9, None],
        [None, None, None, None, None, None, 2, None, None],
        [None, None, 6, None, None, None, 8, None, 7],
        [None, None, None, 3, 1, 6, None, 5, 9],
    ]

    game_state = deserialize_game_state(game_as_text)
    assert get_columns(game_state) == expected


def test_get_rows():
    game_as_text = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    expected = [
        [5, 3, None, None, 7, None, None, None, None],
        [6, None, None, 1, 9, 5, None, None, None],
        [None, 9, 8, None, None, None, None, 6, None],
        [8, None, None, None, 6, None, None, None, 3],
        [
            4,
            None,
            None,
            8,
            None,
            3,
            None,
            None,
        ],
        [7, None, None, None, 2, None, None, None, 6],
        [None, 6, None, None, None, None, 2, 8, None],
        [None, None, None, 4, 1, 9, None, None, 5],
        [None, None, None, None, 8, None, None, 7, 9],
    ]

    game_state = deserialize_game_state(game_as_text)
    assert get_rows(game_state) == expected


def test_get_regions():
    game_as_text = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    expected = [
        [5, 3, None, 6, None, None, None, 9, 8],
        [None, 7, None, 9, 5, None, None, None, None],
        [None, None, None, None, None, None, None, 6, None],
        [8, None, None, 4, None, None, 7, None, None],
        [None, 6, None, 8, None, 3, None, 2, None],
        [None, None, 3, None, None, None, None, 6],
        [None, 6, None, None, None, None, None, None, None],
        [None, None, None, 4, 1, 9, None, 8, None],
        [2, 8, None, None, None, 5, None, 7, 9],
    ]

    game_state = deserialize_game_state(game_as_text)
    assert get_regions(game_state) == expected


def test_is_game_over():
    game_as_text = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    assert is_game_over(deserialize_game_state(game_as_text)) is False


def test_is_game_over_with_full_board():
    game_as_text = """534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179"""
    assert is_game_over(deserialize_game_state(game_as_text)) is True


"""
53..7....
6..195...
.98....6.
8...6...3
4..8.3.
7...2...6
.6....28.
...419..5
....8..79
"""
# ->
# 5 -> []
# 3 -> []
# . -> , 2, 4]
# . -> [5]


def test_is_valid():
    assert is_valid([]) == False
    assert is_valid([None] * 9) == True
    assert is_valid([1, 2, 3, None, None, None, None, None, None]) == True
    assert is_valid([1, 2, 3, 3, None, None, None, None, None]) == False
    assert is_valid([1, 2, 3, 4, 5, 6, 7, 8, 9]) == True
    assert is_valid([1, 2, 3, 4, 5, 6, 7, 8, 9]) == False
    assert is_valid([1] * 9) == False


# solve(
#     deserialize_game_state(
#         """534678912
# 672195348
# 198342567
# 859761423
# 426853791
# 713924856
# 961537284
# 287419635
# 345286179"""
#     )
# )

solve(
    deserialize_game_state(
        """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""
    )
)
