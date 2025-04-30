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

    // Ask user to choose difficulty
    int difficulty = 2;  // Default: Medium
    char* difficulty_label = "Medium";

    printf("Select Difficulty:\n1. Easy\n2. Medium\n3. Hard\nYour choice: ");
    scanf("%d", &difficulty);

    // Set game parameters based on difficulty
    int starting_fuel = 30;
    int win_score = 5;

    if (difficulty == 1) {
        starting_fuel = 40;
        win_score = 3;
        difficulty_label = "Easy";
        printf("You chose EASY mode. Fuel: 40, Score to win: 3\n");
    } else if (difficulty == 3) {
        starting_fuel = 20;
        win_score = 7;
        difficulty_label = "Hard";
        printf("You chose HARD mode. Fuel: 20, Score to win: 7\n");
    } else {
        difficulty_label = "Medium";
        printf("You chose MEDIUM mode. Fuel: 30, Score to win: 5\n");
    }

    // Setup game with default fuel value (to be updated with difficulty later)
    setup_game(&player, &asteroid, &alien, junk, MAX_JUNK, 30);

    int turn = 0;  // To control alien movement every 2 turns

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


         // Movement was valid — apply game updates
         move_asteroid(&asteroid);
         reduce_fuel(&player);
         collect_junk(&player, junk, MAX_JUNK);
 
 
         // Check collision with asteroid
         if (check_collision(player, asteroid)) {
             printf("Game Over! You collided with the asteroid!\n"); fflush(stdout);
             break;
         }
 
         // Check fuel exhaustion
         if (player.fuel <= 0) {
             printf("Game Over! You ran out of fuel.\n"); fflush(stdout);
             break;
         }

        // Move alien every 2 turns
        if (turn % 2 == 0) {
            move_alien(&alien);
        }

        turn++;
    }
    
    // Save score after game ends
    save_score_to_file("scores.txt", player_name, player.score, difficulty_label, player.fuel, player.health, player.x, player.y);

    return 0;
}
