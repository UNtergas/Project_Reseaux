#include "Player.h"
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int isNA(Player player) {
    if (player.ipAddr == NULL || player.name == NULL) {
        return 1;
    }
    return 0;
}

Player initPlayer(char* ipAddr, char* name) {
    Player newPlayer = {NULL, NULL};
    
    unsigned long ip_length = strlen(ipAddr);
    newPlayer.ipAddr = malloc(ip_length+1);
    strncpy(newPlayer.ipAddr, ipAddr, ip_length);
    newPlayer.ipAddr[ip_length] = '\0';
    
    unsigned long name_length = strlen(name);
    newPlayer.name = malloc(name_length+1);
    strncpy(newPlayer.name, name, name_length);
    newPlayer.name[name_length] = '\0';
    
    return newPlayer;
}

void copyPlayer(Player *dst, Player *src) {
    // Length of player ip string
    unsigned long ip_length = strlen(src->ipAddr);
    // Length of player name
    unsigned long name_length = strlen(src->name);

    // If destination ip addr was not allocated => allocate
    if (dst->ipAddr == NULL) {
        dst->ipAddr = malloc(ip_length+1);
    }
    // If destination name was not allocated => allocate
    if (dst->name == NULL) {
        dst->name = malloc(name_length+1);
    }

    strncpy(dst->ipAddr, src->ipAddr, ip_length);
    (dst->ipAddr)[ip_length] = '\0';
    
    strncpy(dst->name, src->name, name_length);
    (dst->name)[ip_length] = '\0';
    
}

int cmpPlayer(Player *dst, Player *src) {
    int cmpName = strcmp(dst->name, src->name);
    int cmpIP = strcmp(dst->ipAddr, src->ipAddr);
    if (cmpName != 0 || cmpIP != 0) return 1; // 1 indicates that dst and src are not equal
    return 0; // 0 indicates that dst and src are equal
}


