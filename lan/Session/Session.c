//
//  Session.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "Session.h"
#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <strings.h>
#include <ifaddrs.h>
#include <fcntl.h>


void createSession(int mode) {
    if (mode == 0) {
        // mode = 0 => create room
    } else {
        // mode == 1 => join room
    }
}

Room createRoom(char* roomName, int maxPlayer, Player host) {
    Room newRoom;
    
    // Initialize room name
    unsigned long nameLength = strlen(roomName) + 1;
    newRoom.name = malloc(nameLength);
    strncpy(newRoom.name, roomName, nameLength);
    newRoom.name[nameLength] = '\0';
    
    // Initialize player number
    newRoom.maxPlayer = maxPlayer;
    
    // Initialize players of room
    newRoom.players = malloc(maxPlayer*sizeof(Player));
    
    addPlayer(&newRoom, &host);
    
    
    
    return newRoom;
}

//int joinRoom(Room *room, struct sockaddr_in *host_addr, char *name, char *player_ip) {
//    if (room == NULL) {
//        write(1, "Room is null\n", 13);
//        return -1;
//    }
//
//    int ip_length = sizeof(room->players[0].ip_addr); // players[0] is the first player in the room aka host of room
//    char *ip_addr = malloc(ip_length+1);
//    strncpy(ip_addr, room->players[0].ip_addr, ip_length);
//    ip_addr[ip_length] = '\0';
//
//    // Create new socket
//    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
//    if (socket_fd < 0) {
//        perror("Error creating new socket");
//        return -1;
//    }
//
//    // Connect
//    write(1, "Waiting for connecting to the room...\n", 38);
//    if (connect(socket_fd, (struct sockaddr *)(&host_addr), sizeof(host_addr)) < 0) {
//        perror("Error connecting to server");
//        return -1;
//    }
//    
//    // Add new player to the room
//    Player newPlayer = initPlayer(ip_addr, name);
//    addPlayer(room, &newPlayer);
//    
//    return socket_fd;
//}

void addPlayer(Room *room, Player *newPlayer) {
    if (room->players == NULL) {
        room->players = malloc((room->maxPlayer)*sizeof(Player));
    }
    for (int i=0; i<room->maxPlayer; ++i) {
        if (isNA(room->players[i])) {
            copyPlayer(&room->players[i], newPlayer);
            return;
        }
    }
}


