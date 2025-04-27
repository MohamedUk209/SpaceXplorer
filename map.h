// This header declares the function used to show the map in the terminal

#ifndef MAP_H
#define MAP_H

#include "game.h"  // We need access to Player, Asteroid, and Junk structures

// This function shows the full 18x18 map with all game objects
void display_map(Player player, Asteroid asteroid, Alien alien, Junk junk[], int junk_count);

#endif
