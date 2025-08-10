#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define DEFAULT_DELAY 0.03

void help(char * name){
	fprintf(stderr, "Usage: %s <file> [delay in sec]\n", name);
	fprintf(stderr, "				types the file with given delay between each characters (or with default %6.3f sec)\n", DEFAULT_DELAY );
	fprintf(stderr, "				-h, --help this help\n");
}

int main(int argc, char *argv[]) {
			if (argc < 2 || argc > 3 || ((argc == 3 ) && ( strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0))) {
				help(argv[0]);
				return 1;
				}

				double delay = (argc == 3) ? atof(argv[2]) : DEFAULT_DELAY;
/*
	int c;
	while ((c = getchar()) != EOF) {
		putchar(c);
		fflush(stdout);
		usleep((useconds_t)(delay * 1e6));
	}
*/

	const char *filename = argv[1];
	FILE *f = fopen(filename, "r");
	if (!f) {
		perror("Error in opening input file");
		return 1;
	}

	int c;
	while ((c = fgetc(f)) != EOF) {
		putchar(c);
		fflush(stdout);
		putc(c,stderr);
		fflush(stderr);
		usleep((useconds_t)(delay * 1e6)); // převod sekund na mikrosekundy
	}

	fclose(f);
		return 0;
}
