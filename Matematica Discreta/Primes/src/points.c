#include <points.h>

#include <stdio.h>


void printPoints(point2D * points, int N) {
	printf("x,y\n");

	for (int i = 0; i < N; i++) {
		printf("%ld,%ld\n", points[i].x, points[i].y);
	}
}

