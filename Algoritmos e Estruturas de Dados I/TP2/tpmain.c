#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include "tp.h"


enum Options {
	OPT_EXIT = 0,
	OPT_SET_CODES,
	OPT_SET_CAPACITIES,
	OPT_RESERVE,
	OPT_QUERY_BUS,
	OPT_QUERY_PASSENGER,
	OPT_BOUNDS,
};

#define NUM_BUS 4

void initBuses(bus * buses, int sz);

int main() {
	bus buses[NUM_BUS];

	initBuses(buses, NUM_BUS);

	int opt = OPT_BOUNDS;

	while (true) {
		printf(
			"[%d] Sair\n"
			"[%d] Especificar codigo dos onibus\n"
			"[%d] Especificar capacidade dos onibus\n"
			"[%d] Fazer uma reserva\n"
			"[%d] Buscar um onibus\n"
			"[%d] Buscar passageiro\n",
			OPT_EXIT,
			OPT_SET_CODES,
			OPT_SET_CAPACITIES,
			OPT_RESERVE,
			OPT_QUERY_BUS,
			OPT_QUERY_PASSENGER
		);

		while (opt < 0 || opt >= OPT_BOUNDS) {
			printf("Escolha um menu: > ");
			scanf("%d", &opt);
		}

		switch (opt) {
			case OPT_SET_CODES:
				busSetCodes(buses, NUM_BUS);
				break;

			case OPT_SET_CAPACITIES:
				busSetCapacities(buses, NUM_BUS);
				break;

			case OPT_RESERVE:
				busReserve(buses, NUM_BUS);
				break;

			case OPT_QUERY_BUS:
				busQueryBus(buses, NUM_BUS);
				break;

			case OPT_QUERY_PASSENGER:
				busQueryPassenger(buses, NUM_BUS);
				break;

			case OPT_EXIT:
				return EXIT_SUCCESS;
		}

		opt = OPT_BOUNDS;
	}

	return EXIT_SUCCESS;
}


void initBuses(bus * buses, int sz) {
	for (int i = 0; i < sz; i = i + 1) {
		buses[i].capacity = 45;
		buses[i].countPeople = 0;

		for (int j = 0; j < 45; j = j + 1) {
			for (int k = 0; k < MAX_NAME_LENGTH; k = k + 1) {
				buses[i].people[j][k] = '\0';
			}
		}
	}
}

