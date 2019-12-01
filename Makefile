libsudoku.so: solve.c solve.h
	gcc -shared -o libsudoku.so -fPIC solve.c
