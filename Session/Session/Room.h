//
//  Session.h
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#ifndef Room_h
#define Room_h

#include <stdio.h>

#include "../Player/Player.h"
#include "../Client/Client.h"

typedef struct {
    char* name; // name of room
    int maxPlayer; // maximun number of players in room
    int currentNumber; // current number of players in room
    Player *players; // array of all players in room
} Room;



int isFull(Room room);



Room createRoom(char* roomName, int maxPlayer, Player host);
int destroyRoom(Room* room);

int discorverRoom(char*** hostIPs, char*** roomNames);
int joinRoom(char *hostIPaddr, char *roomName);

int connectToRoomNetwork(Room room, int **clientSocketFds);

int sendRoomIn4(int newPlayerSocketFd, Room room);

void addPlayer(Room *room, Player *newPlayer);

int sendGameStateToNewPlayer(char *encodedGameState, int newPlayerSocketFd);

#endif /* Session_h */
