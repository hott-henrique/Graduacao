#include <primes.h>


bool primesCheck(long N) {
	if (N <= 1) {
		return false;
	}

	for(long i = 2; i <= (N / 2); i = i + 1){
		if (N % i == 0) {
			return false;
		}
	}

	return true;
}

long primesGetNext(long N) {
	if (N < 2) {
		return 2;
	}

	long next = N + 1;

	while (true) {
		if (primesCheck(next)) {
			return next;
		}

		next = next + 1;
	}
}

