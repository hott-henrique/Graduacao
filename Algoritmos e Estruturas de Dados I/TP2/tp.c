#include "tp.h"

#include <stdbool.h>
#include <stdio.h>
#include <string.h>


void busSetCodes(bus * buses, int sz) {
	for (int i = 0; i < sz; i = i + 1) {
		int code = 0;

		printf("Digite o codigo do onibus: ");
		scanf("%d", &code);

		buses[i].identifier = code;
	}
}

void busSetCapacities(bus * buses, int sz) {
	for (int i = 0; i < sz; i = i + 1) {
		int capacity = 0;

		printf("Digite a capacidade para o onibus %d: ", buses[i].identifier);
		scanf("%d", &capacity);

		buses[i].capacity = capacity;
	}
}

void busReserve(bus * buses, int sz) {
	int code = 0;

	printf("Digite o codigo do onibus: ");
	scanf("%d", &code);

	bool hasFound = false;

	for (int i = 0; i < sz; i = i + 1) {
		if (buses[i].identifier == code) {
			code = i;
			hasFound = true;
			break;
		}
	}

	if (!hasFound) {
		fprintf(stderr, "Onibus nao existe: %d\n", code);
		return;
	}

	bus * b = &buses[code];

	if (b->capacity == b->countPeople) {
		fprintf(stderr, "Onibus sem vagas: %d\n", code);
		return;
	}

	printf("Digite o nome do passageiro: ");
	scanf("%"MAX_NAME_LENGTH_STR"s", b->people[b->countPeople]);

	b->countPeople = b->countPeople + 1;

	printf("Reserva confirmada!\n");
}


void busQueryBus(bus * buses, int sz) {
	int code = 0;

	printf("Digite o codigo do onibus: ");
	scanf("%d", &code);

	bool hasFound = false;

	for (int i = 0; i < sz; i = i + 1) {
		if (buses[i].identifier == code) {
			code = i;
			hasFound = true;
			break;
		}
	}

	if (!hasFound) {
		fprintf(stderr, "Onibus nao existe: %d\n", code);
		return;
	}

	bus * b = &buses[code];

	printf("\tVaga | Passageiro\n");
	for (int i = 0; i < b->countPeople; i = i + 1) {
		printf("\t%d | %s\n", i + 1, b->people[i]);
	}
}

void busQueryPassenger(bus * buses, int sz) {
	char name[MAX_NAME_LENGTH];

	printf("Digite o nome do passageiro: ");
	scanf("%"MAX_NAME_LENGTH_STR"s", name);

	printf("\tOnibus | Vaga | Passageiro\n");
	for (int i = 0; i < sz; i = i + 1) {
		bus * b = &buses[i];
		for (int j = 0; j < b->countPeople; j = j + 1) {
			if (strcmp(name, b->people[j]) == 0) {
				printf("\t%d | %d | %s \n", b->identifier, j + 1, name);
			}
		}
	}
}

