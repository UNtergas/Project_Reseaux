//
//  Session.h
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#ifndef Session_h
#define Session_h

#include <stdio.h>
#include "../Player/Player.h"
//#include "../Client/Client.h"

typedef struct
{
    char* name; // name of room
    int maxPlayer; // maximun number of players in room
    Player *players; // array of all players in room
} Room;

void createSession(int mode);

Room createRoom(char* roomName, int maxPlayer, Player host);
void addPlayer(Room* room, Player* player);
int joinRoom(Room *room, struct sockaddr_in *host_addr, char *name, char *player_ip);

#endif /* Session_h */
