#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "solve.h"

int
check(int grid[9][9], int col, int row)
{
	int d, n;
	d = grid[row][col];

	/* Check row */
	n = 0;
	for (int i = 0; i < 9; i++)
		n += (grid[row][i] == d);
	if (n > 1)
		return 0;

	/* Check column */
	n = 0;
	for (int j = 0; j < 9; j++)
		n += (grid[j][col] == d);
	if (n > 1)
		return 0;

	/* Check square */
	int sq_col = 3 * (col / 3);
	int sq_row = 3 * (row / 3);
	n = 0;
	for (int i = sq_row; i < sq_row + 3; i++)
		for (int j = sq_col; j < sq_col + 3; j++)
			n += (grid[i][j] == d);
	if (n > 1)
		return 0;

	return 1;
}

int
solve(int grid[9][9])
{
	struct {
		int col;
		int row;
	} *cur_sq, *empty_squares;

	ptrdiff_t n_empty_squares;

	cur_sq = empty_squares = malloc(81 * sizeof(*empty_squares));

	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			if (grid[i][j] == 0) {
				cur_sq->col = j;
				cur_sq->row = i;
				++cur_sq;
			}
		}
	}

	cur_sq -= (n_empty_squares = cur_sq - empty_squares);

	/* Step through empty squares until grid done (last square checks out) or failure (first square fails 1-9) */
	while (cur_sq >= empty_squares && cur_sq - empty_squares < n_empty_squares) {

		if (++grid[cur_sq->row][cur_sq->col] > 9) { /* If 1-9 checked, reset current square and hop back */
			grid[cur_sq->row][cur_sq->col] = 0;
			--cur_sq;
		} else if (check(grid, cur_sq->col, cur_sq->row)) { /* Else if current value checks out, hop forward */
			++cur_sq;
		}
	}

	return (cur_sq >= empty_squares);
}
