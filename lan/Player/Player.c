#include "Player.h"
#include <string.h>
#include <stdlib.h>

Player initPlayer(char* ip_addr, char* name) {
    Player newPlayer = {NULL, NULL};
    
    unsigned long ip_length = strlen(ip_addr);
    newPlayer.ip_addr = malloc(ip_length+1);
    strncpy(newPlayer.ip_addr, ip_addr, ip_length);
    newPlayer.ip_addr[ip_length] = '\0';
    
    unsigned long name_length = strlen(name);
    newPlayer.name = malloc(name_length+1);
    strncpy(newPlayer.name, name, name_length);
    newPlayer.name[name_length] = '\0';
    
    return newPlayer;
}

void copyPlayer(Player *dst, Player *src) {

    // Length of player ip string
    unsigned long ip_length = strlen(src->ip_addr);
    // Length of player name
    unsigned long name_length = strlen(src->name);

    // If destination ip addr was not allocated => allocate
    if (dst->ip_addr == NULL) {
        dst->ip_addr = malloc(ip_length+1);
    }
    // If destination name was not allocated => allocate
    if (dst->name == NULL) {
        dst->name = malloc(name_length+1);
    }

    strcpy(dst->ip_addr, src->ip_addr);
    (dst->ip_addr)[ip_length] = '\0';
    
    strcpy(dst->name, src->name);
    (dst->name)[ip_length] = '\0';

    
}

int cmpPlayer(Player *dst, Player *src) {
    int cmpName = strcmp(dst->name, src->name);
    int cmpIP = strcmp(dst->ip_addr, src->ip_addr);
    if (cmpName != 0 || cmpIP != 0) return 1; // 1 indicates that dst and src are not equal
    return 0; // 0 indicates that dst and src are equal
}

void addPlayer(Room* room, Player* newPlayer) {
    for (int i=0; i<room->maxPlayer; ++i) {
        if (cmpPlayer(&room->players[i], &null_player) == 0) {
            copyPlayer(&room->players[i], newPlayer);
            return;
        }
    }
}
