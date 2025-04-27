#include <stdlib.h>
#include <time.h>
#include "game.h"

// This function sets up the starting positions for the player, asteroid, and junk.
// It also uses a custom fuel value passed from main() (based on difficulty selected)
void setup_game(Player* player, Asteroid* asteroid) {
    // Seed the random number generator using system time
    srand(time(NULL));

    // Start player in the center of the map
    player->x = MAP_SIZE / 2;
    player->y = MAP_SIZE / 2;
    player->fuel = 30; // Use starting fuel based on difficulty
    player->score = 0;

    // Place asteroid in bottom-right corner (opposite of player)
    asteroid->x = MAP_SIZE - 1;
    asteroid->y = MAP_SIZE - 1;
}

