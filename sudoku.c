#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct Coord {
	int col;
	int row;
};

int solve(int grid[9][9]);
int check(int grid[9][9], struct Coord *c);
void print_grid(int grid[9][9]);

int main(int argc, char **argv)
{
	int solved;
	clock_t t1, t2;

	int grid[9][9] = {
		{ 0, 0, 2, 0, 9, 0, 0, 0, 5 },
		{ 0, 0, 0, 4, 0, 0, 0, 0, 8 },
		{ 4, 0, 8, 5, 0, 0, 0, 6, 0 },
		{ 0, 4, 0, 0, 2, 0, 0, 0, 0 },
		{ 5, 0, 3, 0, 0, 0, 7, 0, 1 },
		{ 0, 0, 0, 0, 5, 0, 0, 8, 0 },
		{ 0, 6, 0, 0, 0, 3, 8, 0, 9 },
		{ 2, 0, 0, 0, 0, 6, 0, 0, 0 },
		{ 7, 0, 0, 0, 1, 0, 4, 0, 0 },
	};

	/* read_sudoku_file(grid); */

	t1 = clock();
	solved = solve(grid);
	t2 = clock();

	print_grid(grid);
	printf("%s\n", solved ? "Success!" : "Fail :-(");
	printf("Time: %.4fms\n", ((double) (t2 - t1)) / CLOCKS_PER_SEC);
}


int
solve(int grid[9][9])
{
	struct Coord *cur_sq, *empty_squares;
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

	/* for (int i = 0; i < 9; i++) */
	/* 	for (int j = 0; j < 9; j++) */
	/* 		printf("%d\n", grid[i][j]); */

	/* Step through empty squares until grid done or failure (first square fails 1-9) */
	while (cur_sq >= empty_squares && cur_sq - empty_squares < n_empty_squares) {

		/* If 1-9 checked, reset current square and hop back */
		if (++grid[cur_sq->row][cur_sq->col] > 9) {
			grid[cur_sq->row][cur_sq->col] = 0;
			--cur_sq;

		/* Else if current value checks out, hop forward */
		} else if (check(grid, cur_sq)) {
			++cur_sq;
		}
	}

	return (cur_sq >= empty_squares);
}


int
check(int grid[9][9], struct Coord *c)
{
	int d, n;
	d = grid[c->row][c->col];

	/* Check row */
	n = 0;
	for (int i = 0; i < 9; i++)
		n += (grid[c->row][i] == d);
	if (n > 1)
		return 0;

	/* Check column */
	n = 0;
	for (int j = 0; j < 9; j++)
		n += (grid[j][c->col] == d);
	if (n > 1)
		return 0;

	/* Check square */
	int sq_col = 3 * (c->col / 3);
	int sq_row = 3 * (c->row / 3);
	n = 0;
	for (int i = sq_row; i < sq_row + 3; i++)
		for (int j = sq_col; j < sq_col + 3; j++)
			n += (grid[i][j] == d);
	if (n > 1)
		return 0;

	return 1;
}


void print_grid(int grid[9][9])
{
	char hl[] = "+-------+-------+-------+\n";
	for (int i = 0; i < 9; i++) {
		if (i % 3 == 0)
			printf(hl);
		for (int j = 0; j < 3; j++)
			printf("| %d %d %d ", grid[i][3*j], grid[i][3*j+1], grid[i][3*j+2]);
		printf("|\n");
	}
	printf(hl);
}
