#!/usr/bin/env python

import time, os


def read_sudoku_file(sudoku_file):
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


def check(g, index):
    cur_digit = g[index]
    cur_col, cur_row = index % 9, index // 9

    # Check in row
    if g[cur_row*9:(cur_row+1)*9].count(cur_digit) > 1:
        return False

    # Check in column
    if g[cur_col:cur_col+81:9].count(cur_digit) > 1:
        return False

    # Check in square
    sq_col, sq_row = 3 * (cur_col // 3), 3 * (cur_row // 3)
    cur_sq = sum([g[r*9+sq_col:r*9+sq_col+3] for r in range(sq_row, sq_row + 3)], [])
    if cur_sq.count(cur_digit) > 1:
        return False

    return True


def solve(g):
    empty_positions = [i for i, _ in filter(lambda d: d[1] == 0, enumerate(g))]
    cur_square_pointer = 0

    # Step through empty squares
    while 0 <= cur_square_pointer < len(empty_positions):

        # Increment current square
        cur_square = empty_positions[cur_square_pointer]
        g[cur_square] += 1

        # If 1-9 checked, reset and move back
        if g[cur_square] > 9:
            g[cur_square] = 0
            cur_square_pointer -= 1

        # Else move forward if current number checks out
        elif check(g, cur_square):
            cur_square_pointer += 1


g = read_sudoku_file('sudoku.txt')
solve(g)
print_grid(g)
