#ifndef PLAYER_H
#define PLAYER_H

#include <stdio.h>

// A player is the player in this session game
// A player is modeled by a struct (aka class in object-oriented design) with name and ip address used to identify the player in game
typedef struct {
    char* ip_addr;
    char* name;
} Player;

Player null_player = {NULL, NULL};

typedef struct
{
    char* name; // name of room
    int maxPlayer; // maximun number of players in room
    Player *players; // array of all players in room
} Room;

Player initPlayer(char* ip_addr, char* name);

void copyPlayer(Player *dst, Player *src);
int cmpPlayer(Player *dst, Player *src);

void addPlayer(Room* room, Player* player);

#endif
