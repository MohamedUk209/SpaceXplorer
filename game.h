// This header file defines the core structures (Player, Asteroid, Junk)
// and declares functions that handle game setup and logic

#ifndef GAME_H
#define GAME_H

#define MAP_SIZE 18      // The minimum size of the space grid

// This structure keeps track of the player (you, the astronaut)
typedef struct {
    int x;        // Player's horizontal position on the map
    int y;        // Player's vertical position on the map
    int fuel;     // Fuel level, decreases each move
    int score;    // Score increases when junk is collected
} Player;

// This structure represents the dangerous asteroid
typedef struct {
    int x;        // Asteroid's horizontal position
    int y;        // Asteroid's vertical position
} Asteroid;

// Sets up the initial state of the game
void setup_game(Player* player, Asteroid* asteroid);

#endif
