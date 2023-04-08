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
#include <sys/time.h>
#include <pthread.h>


int isFull(Room room) {
    if (room.maxPlayer == room.currentNumber) return 1;
    return 0;
}

Room initRoom(void) {
    Room newRoom;
    newRoom.name = NULL;
    newRoom.maxPlayer = 0;
    newRoom.currentNumber = 0;
    newRoom.players = NULL;
    return newRoom;
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

    newRoom.currentNumber = 0;
    
    // Initialize players of room
    newRoom.players = malloc(maxPlayer*sizeof(Player));
    for (int i=0; i<maxPlayer; ++i) {
        newRoom.players[i].ipAddr = NULL;
        newRoom.players[i].name = NULL;
    }
    
    addPlayer(&newRoom, &host);

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
    if (room == NULL) {
        return 0;
    }
    free(room->name);
    free(room->players);
    room->players = NULL;
    room->currentNumber = 0;
    return 1;
}




// The function @joinRoom is used to request joining into a room
// @parameters: {
//  @hostIPaddr: the IP address of room's host 
// }
// @return: 0 if successfully join of -1 if not
// int joinRoom(char *hostIPaddr, char *roomName) {
//     // Step 1: connect with host via @hostIPaddr (using TCP socket)
//     // Step 2: send the joining request message
//     //      The message's content: ?Join{@roomName} 
//     //      replace the {@roomName} with @roomName
//     // Step 3: wait for response
//     // Step 4: decode response message
//     // Step 5: call @connectToRoomNetwork function to connect with the rest of room

   
//     // Step 1: connect with host via @hostIPaddr (using TCP socket)
//     int sockfd = socket(AF_INET, SOCK_STREAM, 0);
//     if (sockfd < 0) {
//         perror("Failed to create socket");
//         return -1;
//     }

//     struct sockaddr_in servaddr;
//     memset(&servaddr, 0, sizeof(servaddr));
//     servaddr.sin_family = AF_INET;
//     servaddr.sin_port = htons(88888);

//     if (inet_pton(AF_INET, hostIPaddr, &servaddr.sin_addr) <= 0) {
//         perror("Invalid address/ Address not supported");
//         close(sockfd);
//         return -1;
//     }

//     if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
//         perror("Failed to connect");
//         close(sockfd);
//         return -1;
//     }

//     // Step 2: send the joining request message
//     char message[1024];
//     sprintf(message, "?Join{%s}", roomName);

//     if (send(sockfd, message, strlen(message), 0) < 0) {
//         perror("Failed to send joining request message");
//         close(sockfd);
//         return -1;
//     }

//     // Step 3: wait for response
//     char buffer[1024];
//     memset(buffer, 0, sizeof(buffer));
//     if (recv(sockfd, buffer, sizeof(buffer), 0) < 0) {
//         perror("Failed to receive response message");
//         close(sockfd);
//         return -1;
//     }

//     // Step 4: decode response message
//     if (strcmp(buffer, "?JoinAccept") != 0) {
//         printf("Join request denied by host\n");
//         close(sockfd);
//         return -1;
//     }

//     // Step 5: call @connectToRoomNetwork function to connect with the rest of room
//     int result = connectToRoomNetwork(sockfd);
//     if (result < 0) {
//         perror("Failed to connect to room network");
//         close(sockfd);
//         return -1;
//     }

//     return sockfd;
// }





// The function @connectToRoomNetwork is used to connect to the rest of room (except host) 
// The purpose is create a P2P network in room
// @parameters: {
//  @room: the room we want to connect to create a P2P network
//  @clientSocketFds: the list of used to write the new sockets we will create into
// }
// int connectToRoomNetwork(Room room, int **clientSocketFds) {
//     // Step 1: verify if @clientSocketFds is NULL, if yes => return -1
//     // Step 2: verify if *clientSocketFds is NULL, if yes => allocate it as an array of @room.maxPlayer element
//     // Step 3: check if the current number of players of rooms (@room.currentNumber) is 2 or not?
//     //      If yes, return 0 (2 means that the room contains only host and this players)
//     // Step 4: do a for loop to create new connections to all of the members of room
//     //      except the first and the last one (because they are the host and this player)
//     // Step 5: write new created socket into *clientSocketFds
    
    
//     // Step 1: verify if @clientSocketFds is NULL, if yes => return -1
//     if (clientSocketFds == NULL) {
//         return -1;
//     }
    
//     // Step 2: verify if *clientSocketFds is NULL, if yes => allocate it as an array of @room->maxPlayer element
//     if (*clientSocketFds == NULL) {
//         *clientSocketFds = malloc(room->maxPlayer * sizeof(int));
//         if (*clientSocketFds == NULL) {
//             return -1;
//         }
//     }
    
//     // Step 3: check if the current number of players of rooms (@room->currentNumber) is 2 or not?
//     //      If yes, return 0 (2 means that the room contains only host and this player)
//     if (room->currentNumber == 2) {
//         return 0;
//     }
    
//     // Step 4: do a for loop to create new connections to all of the members of room
//     //      except the first and the last one (because they are the host and this player)
//     int i, fd;
//     struct sockaddr_in servAddr;
//     for (i = 1; i < room->currentNumber - 1; i++) {
//         // Create a new socket
//         fd = socket(AF_INET, SOCK_STREAM, 0);
//         if (fd < 0) {
//             return -1;
//         }
        
//         // Set the socket address
//         memset(&servAddr, 0, sizeof(servAddr));
//         servAddr.sin_family = AF_INET;
//         servAddr.sin_addr.s_addr = inet_addr(room->players[i].ipAddr);
//         servAddr.sin_port = htons(PORT);
        
//         // Connect to the server
//         if (connect(fd, (struct sockaddr*)&servAddr, sizeof(servAddr)) < 0) {
//             close(fd);
//             return -1;
//         }
        
//         // Write the new socket into *clientSocketFds
//         (*clientSocketFds)[i] = fd;
//     }
    
//     return 0;

    


// }



// The function @sendRoomIn4 is used to send the current room's information to the new player who just join the room
// @parameters: {
//  @newPlayerSocketFd: the socket fd of new player
//  @room: the information of current room
// }
// @return: 0 if successfully send the room's in4 or -1 if not
// int sendRoomIn4(int newPlayerSocketFd, Room room) {
//     // Step 1: encoded room's in4 by calling the function @roomToStr from MSGCode module
//     // Step 2: send the new encoding message to new player via @newPlayerSocketFd

//     // Step 1: encode room's in4 by calling the function @roomToStr from MSGCode module
//     char *roomIn4 = roomToStr(&room);

//     // Step 2: send the new encoding message to new player via @newPlayerSocketFd
//     if (send(newPlayerSocketFd, roomIn4, strlen(roomIn4), 0) < 0) {
//         perror("Failed to send room in4");
//         return -1;
//     }

//     return 0;
// }



void addPlayer(Room *room, Player *newPlayer) {
    if (isFull(*room)) return;
    
    for (int i=0; i<room->maxPlayer; i++) {
        if (isNA(room->players[i])) {
            copyPlayer(&(room->players[i]), newPlayer);
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
    // Get the length of the encoded game state string
    int len = strlen(encodedGameState);
    
    // Send the length of the message first
    int len_sent = send(newPlayerSocketFd, &len, sizeof(len), 0);
    if (len_sent < 0) {
        perror("Error sending message length");
        return -1;
    }
    
    // Send the encoded game state string
    int sent = send(newPlayerSocketFd, encodedGameState, len, 0);
    if (sent < 0) {
        perror("Error sending message");
        return -1;
    }
    
    return 0;
}

