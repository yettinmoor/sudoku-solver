#!/usr/bin/env python

import sys, time, ctypes


def read_sudoku_file(sudoku_file):
    with open(sudoku_file) as f:
        return [[int(d) for d in line.rstrip()] for line in f.readlines()]


def print_grid(grid):
    hl = '+-------' * 3 + '+\n'
    for i, r in enumerate(grid):
        print((hl if i % 3 == 0 else '') + (3 * '| {} {} {} ').format(*r) + '|')
    print(hl.rstrip())


def interactive_input():
    print('Please input nine 9-digit rows representing your grid.',
            'Mark empty squares as 0.')

    g = []
    while len(g) < 9:
        try:
            row = input(f'Row {len(g) + 1}>> ').strip()
        except KeyboardInterrupt:
            exit(1)

        if not row.isdigit() or len(row) != 9:
            print(f'Invalid row: "{row}"')
        else:
            g.append([int(d) for d in row])

    return g


def main():
    if len(sys.argv) == 1:
        g = interactive_input()
    else:
        g = read_sudoku_file(sys.argv[1])

    libsudoku = ctypes.CDLL('./libsudoku.so')

    # Convert grid to C int[9][9]
    c_grid_t = (ctypes.c_int * 9) * 9
    c_grid = c_grid_t(*[(ctypes.c_int * 9)(*r) for r in g])
    libsudoku.solve.argtypes = [c_grid_t]

    t1 = time.time()
    libsudoku.solve(c_grid)
    t2 = time.time()

    # Recovert c_grid to 2D Python list
    g = [[d for d in c_row] for c_row in c_grid]

    print_grid(g)
    print('Time to solve: {:.3}s'.format(t2 - t1))


if __name__ == '__main__':
    main()
