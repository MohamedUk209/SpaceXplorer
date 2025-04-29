#include <stdio.h>
#include "game.h"
#include "map.h"
#include "fileio.h"

int main() {
    Player player;
    Asteroid asteroid;
    Junk junk[MAX_JUNK];
    Alien alien;

    // Ask for player's name
    char player_name[50];
    printf("Enter your name: ");
    scanf("%s", player_name);  // Reads until first space

    // Show the intro story from file
    read_intro_from_file("intro.txt");

    // Setup game with default fuel value (to be updated with difficulty later)
    setup_game(&player, &asteroid, &alien, junk, MAX_JUNK, 30);

    int turn = 0;  // To control alien movement every 2 turns

    // Display the space map and current location
    display_map(player, asteroid, alien, junk, MAX_JUNK);

    while (1) {
         // Display the space map and current location
         display_map(player, asteroid, alien, junk, MAX_JUNK);

        // Ask for movement input
        char move;
        printf("Enter move (W = up, A = left, S = down, D = right): ");
        printf("\nCheck System (H) ");
        scanf(" %c", &move);

        // Check if user wants system status
        if (move == 'H' || move == 'h') {
            // Print health/fuel/score status on demand
            printf("\n--- Ship Status ---\n");
            printf("Location: (%d, %d)\n", player.x, player.y);
            printf("Fuel: %d\n", player.fuel);
            printf("Health: %d\n", player.health);
            printf("Score: %d\n", player.score);
            printf("--------------------\n\n");
            continue;  // Skip the rest of the loop
        }

        // Check for valid movement keys
        if (move != 'W' && move != 'w' &&
            move != 'A' && move != 'a' &&
            move != 'S' && move != 's' &&
            move != 'D' && move != 'd') {
            printf("Invalid input! Use W, A, S, or D.\n");
            continue;
        }

        // Attempt to move the player
        if (!move_player(&player, move)) {
            printf("You hit the boundary! No movement made.\n");  fflush(stdout);
            continue;  // Skip update logic
        }

        // Move alien every 2 turns
        if (turn % 2 == 0) {
            move_alien(&alien);
        }

        turn++;
    }
    

    return 0;
}
