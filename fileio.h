// This header declares functions for reading and writing game-related files

#ifndef FILEIO_H
#define FILEIO_H

// Shows the game intro from a text file
void read_intro_from_file(const char* filename);

// Saves the player's final score to a text file
void save_score_to_file(const char* filename, const char* player_name, int score, const char* difficulty, int fuel, int health, int x, int y);

#endif
