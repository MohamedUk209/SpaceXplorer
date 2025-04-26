#include <stdio.h>
#include "map.h"

// This function draws the space map in the terminal
// It shows the player (P), asteroid (A), junk (J), and empty space (.)
void display_map(Player player, Asteroid asteroid, Alien alien, Junk junk[], int junk_count) {
    // We use a 2D array to represent the space grid
    char grid[MAP_SIZE][MAP_SIZE];

    // Fill grid with empty dots (.)
    for (int y = 0; y < MAP_SIZE; y++) {
        for (int x = 0; x < MAP_SIZE; x++) {
            grid[y][x] = '.';
        }
    }

    // Add space junk to the grid (only if it hasn’t been collected)
    for (int i = 0; i < junk_count; i++) {
        if (!junk[i].collected) {
            grid[junk[i].y][junk[i].x] = 'J';
        }
    }

    // Place asteroid (A) on the map
    grid[asteroid.y][asteroid.x] = 'A';

    // Place alien (X) on the map
    grid[alien.y][alien.x] = 'X';

    // Place player (P) on the map (after all others)
    grid[player.y][player.x] = 'P';

    // Print the grid row by row
    printf("\n--- Space Map ---\n");
    for (int y = 0; y < MAP_SIZE; y++) {
        for (int x = 0; x < MAP_SIZE; x++) {
            printf("%c ", grid[y][x]);
        }
        printf("\n");
    }

    // Print current resource status
    printf("Fuel: %d   Score: %d   Health: %d\n", player.fuel, player.score, player.health);
}
