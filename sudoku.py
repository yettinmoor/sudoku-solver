#!/usr/bin/env python

import sys, time, os


def read_sudoku_file(sudoku_file):
    """ Ex. format:
    002090005
    000400008
    408500060
    040020000
    503000701
    000050080
    060003809
    200006000
    700010400
    """
    grid = []
    with open(sudoku_file) as f:
        for line in f.readlines():
            grid.append([int(d) for d in line[:-1]])
    return grid


def print_grid(grid):
    border = '+' + '-'*23 + '+'
    print(border)
    for i, r in enumerate(grid):
        print('| ', end='')
        for j, d in enumerate(r):
            print(d if d else ' ', end=' | ' if j % 3 == 2 else ' ')
        print()
        if ((i + 1) % 3) == 0:
            print(border)


def check(g, col, row):
    digit = g[row][col]

    # Check in row
    if g[row].count(digit) > 1:
        return False

    # Check in column
    if [r[col] for r in g].count(digit) > 1:
        return False

    # Check in square
    sq_col, sq_row = 3 * (col // 3), 3 * (row // 3)
    sq = sum([r[sq_col:sq_col+3] for r in g[sq_row:sq_row+3]], [])
    if sq.count(digit) > 1:
        return False

    return True


def solve(g):
    # Create list of empty squares
    empty_squares = []
    for i, r in enumerate(g):
        empty_squares += [(j, i) for j, _ in filter(lambda d: d[1] == 0, enumerate(r))]

    cur_empty_sq = 0

    # Step through empty squares
    while 0 <= cur_empty_sq < len(empty_squares):

        # Increment current square
        col, row = empty_squares[cur_empty_sq]
        g[row][col] += 1

        # If 1-9 checked, reset and move back
        if g[row][col] > 9:
            g[row][col] = 0
            cur_empty_sq -= 1

        # Else move forward if current number checks out
        elif check(g, col, row):
            cur_empty_sq += 1


def interactive_input():
    ans = []
    while len(ans) < 9:
        try:
            row = input(f'Row {len(ans)}>> ').strip()
        except KeyboardInterrupt:
            exit(1)

        if not row.isdigit():
            print('Invalid row: "{now}"')
        else:
            ans.append([int(d) for d in row])

    return ans


def main():
    if len(sys.argv) == 1:
        g = interactive_input()
    else:
        g = read_sudoku_file(sys.argv[1])

    t1 = time.time()
    solve(g)

    t2 = time.time()
    print_grid(g)
    print('Time to solve: {:.3}s'.format(t2 - t1))


if __name__ == '__main__':
    main()
