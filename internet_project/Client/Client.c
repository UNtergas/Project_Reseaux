#include "Client.h"
#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <strings.h>


Client initClient(char *ip_addr, char *name, int socket_fd) {
    Player newPlayer = initPlayer(ip_addr, name);
    Client newClient = {NULL, socket_fd};
    newClient.player = malloc(sizeof(Player));
    copyPlayer(newClient.player, &newPlayer);
    return newClient;
}

Room createRoom(char* roomName, Player host) {
    unsigned long nameLength = strlen(roomName) + 1;
    Room newRoom;
    newRoom.name = malloc(nameLength);
    strncpy(newRoom.name, roomName, nameLength);
    newRoom.name[nameLength] = '\0';
    addPlayer(&newRoom, &host);
    return newRoom;
}

int joinRoom(Room *room, struct sockaddr_in *host_addr, char *name, char *player_ip) {
    if (room == NULL) {
        write(1, "Room is null\n", 13);
        return -1;
    }

    int ip_length = sizeof(room->players[0].ip_addr); // players[0] is the first player in the room aka host of room
    char *ip_addr = malloc(ip_length+1);
    strncpy(ip_addr, room->players[0].ip_addr, ip_length);
    ip_addr[ip_length] = '\0';

    // Create new socket
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        perror("Error creating new socket");
        return -1;
    }

    // Connect 
    write(1, "Waiting for connecting to the room...\n", 38);
    if (connect(socket_fd, (struct sockaddr *)(&host_addr), sizeof(host_addr)) < 0) {
        perror("Error connecting to server");
        return -1;
    }
    
    // Add new player to the room
    Player newPlayer = initPlayer(ip_addr, name);
    addPlayer(room, &newPlayer);
    
    return socket_fd;
}

