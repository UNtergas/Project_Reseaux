#ifndef PLAYER_H
#define PLAYER_H

#include <stdio.h>

// A player is the player in this session game
// A player is modeled by a struct (aka class in object-oriented design) with name and ip address used to identify the player in game
typedef struct {
    char* ipAddr;
    char* name;
} Player;



int isNA(Player player);

Player initPlayer(char* ipAddr, char* name);

void copyPlayer(Player *dst, Player *src);
int cmpPlayer(Player *dst, Player *src);

#endif
