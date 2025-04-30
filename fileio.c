#include <stdio.h>
#include "fileio.h"
#include <time.h>

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

// This function writes the player's final score, name, and difficulty to a leaderboard file
void save_score_to_file(const char* filename, const char* player_name, int score, const char* difficulty, int fuel, int health, int x, int y) {
    FILE* file = fopen(filename, "a");  // Append mode

    if (file == NULL) {
        printf("Warning: Could not save score.\n");
        return;
    }

    // Get current date and time
    time_t now = time(NULL);
    struct tm* t = localtime(&now);

    // Write full leaderboard record
    fprintf(file, "Date: %02d-%02d-%04d %02d:%02d:%02d\n", 
        t->tm_mday, t->tm_mon + 1, t->tm_year + 1900,
        t->tm_hour, t->tm_min, t->tm_sec);

    fprintf(file, "Player: %s\n", player_name);
    fprintf(file, "Difficulty: %s\n", difficulty);
    fprintf(file, "Score: %d\n", score);
    fprintf(file, "Final Fuel: %d\n", fuel);
    fprintf(file, "Final Health: %d\n", health);
    fprintf(file, "Final Position: (%d, %d)\n", x, y);
    fprintf(file, "---\n");

    fclose(file);
    printf("Your game summary has been saved to the leaderboard!\n");
}