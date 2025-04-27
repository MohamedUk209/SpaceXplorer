#include <stdio.h>
#include "map.h"

// Display the game map with player and asteroid
void display_map(Player player, Asteroid asteroid) {
    // We use a 2D array to represent the space grid
    char grid[MAP_SIZE][MAP_SIZE];

    // Fill grid with empty dots (.)
    for (int y = 0; y < MAP_SIZE; y++) {
        for (int x = 0; x < MAP_SIZE; x++) {
            grid[y][x] = '.';
        }
    }

    // Place asteroid (A) on the map
    grid[asteroid.y][asteroid.x] = 'A';

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
}
