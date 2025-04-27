#include <stdio.h>
#include "fileio.h"

// This function reads and prints the intro text from a file (like a welcome message)
void read_intro_from_file(const char* filename) {
    FILE* file = fopen(filename, "r");

    if (file == NULL) {
        printf("Warning: Could not open intro file.\n");
        return;
    }

    char line[256];  // Read one line at a time (max 255 chars per line)
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);  // Print the line to the screen
    }

    fclose(file);
}
