#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "game.h"

// This function sets up the starting positions for the player, asteroid, and junk.
// It also uses a custom fuel value passed from main() (based on difficulty selected)
void setup_game(Player* player, Asteroid* asteroid, Alien* alien, Junk junk[], int junk_count, int fuel) {
    // Seed the random number generator using system time
    srand(time(NULL));

    // Start player in the center of the map
    player->x = MAP_SIZE / 2;
    player->y = MAP_SIZE / 2;
    player->fuel = fuel;      // Use starting fuel based on difficulty
    player->score = 0;
    player->health = 10;      // Starting health for the ship

    // Place asteroid in bottom-right corner (opposite of player)
    asteroid->x = MAP_SIZE - 1;
    asteroid->y = MAP_SIZE - 1;

    // Place each junk in a random empty position
    for (int i = 0; i < junk_count; i++) {
        int valid = 0;

        // Keep trying until we find a valid spot
        while (!valid) {
            int x = rand() % MAP_SIZE;
            int y = rand() % MAP_SIZE;

            valid = 1;

            // Avoid player's position
            if (x == player->x && y == player->y)
                valid = 0;

            // Avoid asteroid's position
            if (x == asteroid->x && y == asteroid->y)
                valid = 0;

            // Avoid overlapping with other junk
            for (int j = 0; j < i; j++) {
                if (junk[j].x == x && junk[j].y == y) {
                    valid = 0;
                    break;
                }
            }

            // If it's valid, assign position and mark as not collected
            if (valid) {
                junk[i].x = x;
                junk[i].y = y;
                junk[i].collected = 0;
            }
        }
    }

    // Place alien in a random position that doesn't overlap anything else
    int placed = 0;
    while (!placed) {
        int x = rand() % MAP_SIZE;
        int y = rand() % MAP_SIZE;

        int valid = 1;

        // Avoid player
        if (x == player->x && y == player->y) valid = 0;
        // Avoid asteroid
        if (x == asteroid->x && y == asteroid->y) valid = 0;
        // Avoid junk
        for (int j = 0; j < junk_count; j++) {
            if (junk[j].x == x && junk[j].y == y) {
                valid = 0;
                break;
            }
        }

        if (valid) {
            alien->x = x;
            alien->y = y;
            placed = 1;
        }
    }
}

// This function moves the player based on input (W = up, A = left, S = down, D = right)
int move_player(Player* player, char direction) {
    int new_x = player->x;
    int new_y = player->y;

    switch (direction) {
        case 'W':
        case 'w': new_y--; break;
        case 'S':
        case 's': new_y++; break;
        case 'A':
        case 'a': new_x--; break;
        case 'D':
        case 'd': new_x++; break;
        default: return 0;  // Invalid direction
    }

    if (new_x >= 0 && new_x < MAP_SIZE && new_y >= 0 && new_y < MAP_SIZE) {
        player->x = new_x;
        player->y = new_y;
        return 1;  // Move succeeded
    } else {
        return 0;  // Hit boundary
    }
}

// This function moves the asteroid one cell up (just for now, we’ll improve this later)
void move_asteroid(Asteroid* asteroid) {
    if (asteroid->y > 0) {
        asteroid->y--; // Slowly creeps up toward the player
    }
}

// This function reduces fuel every turn
void reduce_fuel(Player* player) {
    if (player->fuel > 0) {
        player->fuel--;
    }
}

// This function checks if the player is on the same cell as any uncollected junk
void collect_junk(Player* player, Junk junk[], int junk_count) {
    for (int i = 0; i < junk_count; i++) {
        // Check if junk is on the player's tile and not already collected
        if (!junk[i].collected && junk[i].x == player->x && junk[i].y == player->y) {
            junk[i].collected = 1;     // Mark as collected
            player->score++;           // Increase score

            // Ask the player how to use the junk
            printf("You collected space junk! Choose action:\n"); fflush(stdout);
            printf("F = +5 Fuel\n"); fflush(stdout);
            printf("R = +2 Repair (Health)\n"); fflush(stdout);
            printf("Your choice: "); fflush(stdout);

            char choice;
            scanf(" %c", &choice);  // Space before %c ignores leftover newline

            if (choice == 'F' || choice == 'f') {
                player->fuel += 5;
                printf("You gained +5 fuel!\n"); fflush(stdout);
            } else if (choice == 'R' || choice == 'r') {
                player->health += 2;
                printf("You repaired the ship! +2 health.\n"); fflush(stdout);
            } else {
                // Default fallback
                player->fuel += 5;
                printf("Invalid choice. Defaulted to +5 fuel.\n"); fflush(stdout);
            }
        }
    }
}

// This function checks if the player and asteroid are in the same position
int check_collision(Player player, Asteroid asteroid) {
    return (player.x == asteroid.x && player.y == asteroid.y);
}

// This function checks if the player has reached the win condition
int check_win(Player player) {
    return (player.score >= 5); // win if you collect 5 junk pieces
}

void move_alien(Alien* alien) {
    int direction = rand() % 4;
    if (direction == 0 && alien->y > 0) alien->y--;              // Up
    else if (direction == 1 && alien->y < MAP_SIZE - 1) alien->y++; // Down
    else if (direction == 2 && alien->x > 0) alien->x--;              // Left
    else if (direction == 3 && alien->x < MAP_SIZE - 1) alien->x++;   // Right
}

