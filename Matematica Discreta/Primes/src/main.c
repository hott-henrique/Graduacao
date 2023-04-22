#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

#include <primes.h>
#include <points.h>


bool analyseInput(long input);

void assurePrimePoint(point2D * p);

void getNextNPrimePairs(point2D * outPoints, long N, point2D startingPoint);

int main(int argc, char * argv[]) {
	if (argc != 3) {
		fprintf(stderr, "Usage: %s <NUMBER OF POINTS> <N>\n", argv[0]);
		return EXIT_FAILURE;
	}

	long numberOfPairs = strtol(argv[1], NULL, 10);

	if (numberOfPairs <= 1)
		numberOfPairs = 2;

	if (!analyseInput(numberOfPairs)) {
		fprintf(stderr, "Error parsing number of pairs: %s\n", argv[1]);
		return EXIT_FAILURE;
	}

	long xFirstPoint = strtol(argv[2], NULL, 10);

	if (!analyseInput(xFirstPoint)) {
		fprintf(stderr, "Error parsing x for starting point: %s\n", argv[2]);
		return EXIT_FAILURE;
	}

	long yFirstPoint = 0;

	point2D firstPoint = { xFirstPoint, yFirstPoint };

	assurePrimePoint(&firstPoint);

	point2D listOfPairs[numberOfPairs + 1]; listOfPairs[0] = firstPoint;

	getNextNPrimePairs(listOfPairs, numberOfPairs + 1, firstPoint);

	printPoints(listOfPairs, numberOfPairs);

	return 0;
}

bool analyseInput(long input) {
	if (input <= 0) {
		return false;
	}

	return true;
}

void assurePrimePoint(point2D * P) {
	if (!primesCheck(P->x)) {
		P->x = primesGetNext(P->x);
	}

	P->y = primesGetNext(P->x);
}

void getNextNPrimePairs(point2D* outPairs, long N, point2D startingPoint) {
	long currentPrime = startingPoint.y;

	for (long i = 0; i < N; i = i + 1) {
		outPairs[i].x = currentPrime;
		currentPrime = primesGetNext(currentPrime);

		outPairs[i].y = currentPrime;
		currentPrime = primesGetNext(currentPrime);
	}
}

