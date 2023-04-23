#ifndef TP_HEADER_FILE
#define TP_HEADER_FILE

#define MAX_NAME_LENGTH 256
#define MAX_NAME_LENGTH_STR "255"

typedef struct bus_t {
	int identifier;
	int capacity;
	int countPeople;
	char people[45][MAX_NAME_LENGTH];
} bus;

void busSetCodes(bus * buses, int sz);

void busSetCapacities(bus * buses, int sz);

void busReserve(bus * buses, int sz);

void busQueryBus(bus * buses, int sz);

void busQueryPassenger(bus * buses, int sz);

#endif

