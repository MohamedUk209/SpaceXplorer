#include <stdio.h>
#include "map.h"

// This function draws the space map in the terminal
// It shows the player (P), asteroid (A), alien (X), junk (J), and empty spaces (.)
void display_map(Player player, Asteroid asteroid, Alien alien, Junk junk[], int junk_count) {
    // Initialize the grid with empty spaces
    char grid[MAP_SIZE][MAP_SIZE];

    // Fill grid with empty dots (.)
    for (int y = 0; y < MAP_SIZE; y++) {
        for (int x = 0; x < MAP_SIZE; x++) {
            grid[y][x] = '.';
        }
    }

    // Add junk to the map if not collected
    for (int i = 0; i < junk_count; i++) {
        if (!junk[i].collected) {
            grid[junk[i].y][junk[i].x] = 'J';
        }
    }

    // Place asteroid
    grid[asteroid.y][asteroid.x] = 'A';

    // Place alien
    grid[alien.y][alien.x] = 'X';

    // Place player last
    grid[player.y][player.x] = 'P';

    // Print the grid
    printf("\n--- Space Map ---\n");
    for (int y = 0; y < MAP_SIZE; y++) {
        for (int x = 0; x < MAP_SIZE; x++) {
            printf("%c ", grid[y][x]);
        }
        printf("\n");
    }

    // Print player status
    printf("Fuel: %d   Score: %d   Health: %d\n", player.fuel, player.score, player.health);
}
