#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>


#define N 20

enum Options {
	EXIT = 0,
	FILL = 1,
	PRINT_ALL = 2,
	PRINT_WOMAN_GREATEST_CR = 3,
	PRINT_COURSES_UID = 4,
	OPTIONS_BOUND,
};

enum Columns {
	REGISTRATION_COLUMN,
	COURSE_COLUMN,
	GENDER_COLUMN,
	CR_COLUMN,
};

enum Gender {
	MALE = 0,
	FEMALE = 1
};

int main() {
	bool wasFilled = false;

	int sigaa[N][4];

	int option = OPTIONS_BOUND;

	while (true) {
		printf(
			"[%d] Fill system.\n"
			"[%d] Print system.\n"
			"[%d] Print woman with greatest cr in course.\n"
			"[%d] Print available courses.\n"
			"[%d] Exit\n",
			FILL, PRINT_ALL, PRINT_WOMAN_GREATEST_CR, PRINT_COURSES_UID, EXIT
		);
		while (option >= OPTIONS_BOUND) {
			printf("Type an option: > ");
			scanf("%d", &option);
		}

		switch (option) {
			case FILL: {
				for (int i = 0; i < N; i = i + 1) {
					printf("Filling for student: %d\n", i + 1);

					int * row = sigaa[i];

					printf("Type the course indentifier: "); scanf("%d", &row[COURSE_COLUMN]);

					row[GENDER_COLUMN] = -1;
					while (row[GENDER_COLUMN] != 0 && row[GENDER_COLUMN] != 1) {
						printf("Type the gender - 0[M] or 1[F]: "); scanf("%d", &row[GENDER_COLUMN]);
					}

					printf("Type the CR: "); scanf("%d", &row[CR_COLUMN]);

					printf("Type the student registration: "); scanf("%d", &row[REGISTRATION_COLUMN]);
				}

				wasFilled = true;
				break;
			}

			case PRINT_ALL: {
				if (!wasFilled) {
					printf("Please, fill the system first.\n");
					break;
				}

				printf("Course | Gender | Registration | CR\n");
				for (int i = 0; i < N; i = i + 1) {
					int * row = sigaa[i];
					printf(
						"%d | %c | %d | %d\n",
						row[COURSE_COLUMN],
						row[GENDER_COLUMN] == MALE ? 'M' : 'F',
						row[REGISTRATION_COLUMN],
						row[CR_COLUMN]
					);
				}

				break;
			}

			case PRINT_COURSES_UID: {
				if (!wasFilled) {
					printf("Please, fill the system first.\n");
					break;
				}

				printf("Available courses: ");

				for (int i = 0; i < N; i = i + 1) {
					bool hasAppeared = false;

					int * rowI = sigaa[i];

					for (int j = 0; j < i; j = j + 1) {
						int * rowJ = sigaa[j];

						if (rowI[COURSE_COLUMN] == rowJ[COURSE_COLUMN]) {
							hasAppeared = true;
							break;
						}
					}

					if (!hasAppeared) {
						printf("%d ", rowI[COURSE_COLUMN]);
					}
				}

				putchar('\n');

				break;
			}

			case PRINT_WOMAN_GREATEST_CR: {
				if (!wasFilled) {
					printf("Please, fill the system first.\n");
					break;
				}

				int course;
				printf("Type the course indentifier: "); scanf("%d", &course);

				bool hasFound = 0;
				int cr = 0;
				int studentRegistration = 0;

				for (int i = 1; i < N; i = i + 1) {
					int * rowI = sigaa[i];

					if (rowI[GENDER_COLUMN] == FEMALE && rowI[COURSE_COLUMN] == course) {
						if (!hasFound || rowI[CR_COLUMN] > cr) {
							hasFound = true;
							cr = rowI[CR_COLUMN];
							studentRegistration = rowI[REGISTRATION_COLUMN];
							continue;
						}
					}
				}

				if (!hasFound) {
					printf("There is not a single woman is the system.\n");
					break;
				}

				printf("Registration: %d | CR: %d\n", studentRegistration, cr);

				break;
			}

			case EXIT: {
				return EXIT_SUCCESS;
			}

			default:
				continue;
		}

		option = OPTIONS_BOUND;
	}

	return EXIT_SUCCESS;
}

