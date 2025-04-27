#include <stdio.h>
#include "game.h"
#include "map.h"
#include "fileio.h"

int main() {
    Player player;
    Asteroid asteroid;

    // Ask for player's name
    char player_name[50];
    printf("Enter your name: ");
    scanf("%s", player_name);  // Reads until first space

    read_intro_from_file("intro.txt");

    // Setup game with selected fuel level
    setup_game(&player, &asteroid);

    // Display the space map and current location
    display_map(player, asteroid);

    printf("\nThank you for playing, %s!\n", player_name);

    return 0;
}
