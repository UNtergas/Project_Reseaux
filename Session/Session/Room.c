//
//  Session.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "Room.h"
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

int isFull(Room room) {
    if (room.maxPlayer == room.currentNumber) return 1;
    return 0;
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
    
    newRoom.currentNumber = 1;
    
    return newRoom;
}


// The function @destroyRoom is used to end the current room (current session)
// @parameters: {
//  @room: The room we want to end
// }
int destroyRoom(Room *room) {
    // Step 1: free the @room->name pointer
    // Step 2: free the @room->players pointer
    // Step 3: free the @room pointer

    // +++ YOUR CODE HERE +++ //
}



// The function @discoverRoom is used to discover if there are any active room in current LAN
// @parameters: {
//  @hostIPs: used to write the ip address of discovered room's host
//  @roomNames: used to write the room name of discovered room
// }
// @return: 0 if successfully discorver the rooms or -1 if not
int discorverRoom(char*** hostIPs, char*** roomNames) {
    // Step 1: send to all IP in LAN the following package:
    //      Package's content: ?DiscoverRoom
    // Step 2: wait for the response
    // Step 3: write the response to @hostIPs and @roomNames

    // +++ YOUR CODE HERE +++ //
}



// The function @joinRoom is used to request joining into a room
// @parameters: {
//  @hostIPaddr: the IP address of room's host 
// }
// @return: 0 if successfully join of -1 if not
int joinRoom(char *hostIPaddr, char *roomName) {
    // Step 1: connect with host via @hostIPaddr (using TCP socket)
    // Step 2: send the joining request message
    //      The message's content: ?Join{@roomName} 
    //      replace the {@roomName} with @roomName
    // Step 3: wait for response
    // Step 4: decode response message
    // Step 5: call @connectToRoomNetwork function to connect with the rest of room

    // +++ YOUR CODE HERE +++ //
}



// The function @connectToRoomNetwork is used to connect to the rest of room (except host) 
// The purpose is create a P2P network in room
// @parameters: {
//  @room: the room we want to connect to create a P2P network
//  @clientSocketFds: the list of used to write the new sockets we will create into
// }
int connectToRoomNetwork(Room room, int **clientSocketFds) {
    // Step 1: verify if @clientSocketFds is NULL, if yes => return -1
    // Step 2: verify if *clientSocketFds is NULL, if yes => allocate it as an array of @room.maxPlayer element
    // Step 3: check if the current number of players of rooms (@room.currentNumber) is 2 or not?
    //      If yes, return 0 (2 means that the room contains only host and this players)
    // Step 4: do a for loop to create new connections to all of the members of room
    //      except the first and the last one (because they are the host and this player)
    // Step 5: write new created socket into *clientSocketFds

    // +++ YOUR CODE HERE +++ //
}



// The function @sendRoomIn4 is used to send the current room's information to the new player who just join the room
// @parameters: {
//  @newPlayerSocketFd: the socket fd of new player
//  @room: the information of current room
// }
// @return: 0 if successfully send the room's in4 or -1 if not
int sendRoomIn4(int newPlayerSocketFd, Room room) {
    // Step 1: encoded room's in4 by calling the function @roomToStr from MSGCode module
    // Step 2: send the new encoding message to new player via @newPlayerSocketFd

    // +++ YOUR CODE HERE +++ //
}



void addPlayer(Room *room, Player *newPlayer) {
    if (isFull(*room)) return;
    if (room->players == NULL) {
        room->players = malloc((room->maxPlayer)*sizeof(Player));
    }
    for (int i=0; i<room->maxPlayer; ++i) {
        if (isNA(room->players[i])) {
            copyPlayer(&room->players[i], newPlayer);
            room->currentNumber += 1;
            return;
        }
    }
}



// The function @sendGameStateToNewPlayer is used to send the current game state to the new player of the room
// parameters: {
//  @encodedGameState: the game state encoded under the type of string
//  @newPlayerSocketFd: the socket fd of new player 
// }
// @return: 0 if successfully send or -1 if not
int sendGameStateToNewPlayer(char *encodedGameState, int newPlayerSocketFd) {
    // +++ YOUR CODE HERE +++ //
}

