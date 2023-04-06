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
#define MAX_ROOMS 100

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

    if(room==NULL){
        return 0;
    }
    free(room->name);
    free(room->player);
    room->player=NULL;
    room->currentNumber=0;
    return 1;

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

    // Create a UDP socket for broadcasting
    int sock = socket(AF_INET,SOCK_DGRAM,0);
    if(sock<0){
        perror("failed to create socket");
        return -1;
    }
     // Enable broadcasting on the socket
     int broadcastEnable = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcastEnable, sizeof(broadcastEnable)) < 0) {
        perror("Failed to set socket option");
        close(sock);
        return -1;
    }
    // Set up the broadcast address
    struct sockaddr_in broadcastAddr;
    memset(&broadcastAddr, 0, sizeof(broadcastAddr));
    broadcastAddr.sin_family = AF_INET;
    broadcastAddr.sin_port = htons(PORT);
    broadcastAddr.sin_addr.s_addr = htonl(INADDR_BROADCAST);
    // Send the broadcast message
    char* message = "?DiscoverRoom";
    if (sendto(sock, message, strlen(message), 0, (struct sockaddr*)&broadcastAddr, sizeof(broadcastAddr)) < 0) {
        perror("Failed to send broadcast message");
        close(sock);
        return -1;
    }
    // Set up a socket to receive responses
    struct sockaddr_in recvAddr;
    socklen_t recvAddrLen = sizeof(recvAddr);
    char buffer[1024];
    int numRooms = 0;
    // Receive responses until a timeout occurs or the maximum number of rooms is reached
    while (numRooms < MAX_ROOMS) {
        // Set a timeout for the receive operation
        struct timeval timeout;
        timeout.tv_sec = 5; // Timeout after 5 seconds
        timeout.tv_usec = 0;
        if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
            perror("Failed to set socket option");
            close(sock);
            return -1;
        }
    // Receive a response message
        memset(buffer, 0, sizeof(buffer));
        int numBytes = recvfrom(sock, buffer, sizeof(buffer)-1, 0, (struct sockaddr*)&recvAddr, &recvAddrLen);
        if (numBytes < 0) {
            // Timeout occurred, so we're done
            break;
        }
    // Check if the message is a room discover
        if (strcmp(buffer, "?DiscoverRoom") == 0) {
            // Extract the host IP and room name from the response message
            char* hostIP = inet_ntoa(recvAddr.sin_addr);  //  hostIP now points to a string containing the host IP in dotted decimal format.
            char* roomName = strchr(buffer, ':') + 1;     //  roomName now points to the room name string in the received message.

            // Allocate memory for the host IP and room name strings
            int hostIPLen = strlen(hostIP) + 1;
            int roomNameLen = strlen(roomName) + 1;
            *hostIPs[numRooms] = malloc(hostIPLen);
            *roomNames[numRooms] = malloc(roomNameLen);

            // Copy the host IP and room name into the arrays
            strncpy(*hostIPs[numRooms], hostIP, hostIPLen);
            strncpy(*roomNames[numRooms], roomName, roomNameLen);

            numRooms++;
        }
    } 
    close(sock);
    return numRooms;

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

   
    // Step 1: connect with host via @hostIPaddr (using TCP socket)
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Failed to create socket");
        return -1;
    }

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, hostIPaddr, &servaddr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        close(sockfd);
        return -1;
    }

    if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        perror("Failed to connect");
        close(sockfd);
        return -1;
    }

    // Step 2: send the joining request message
    char message[1024];
    sprintf(message, "?Join{%s}", roomName);

    if (send(sockfd, message, strlen(message), 0) < 0) {
        perror("Failed to send joining request message");
        close(sockfd);
        return -1;
    }

    // Step 3: wait for response
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));
    if (recv(sockfd, buffer, sizeof(buffer), 0) < 0) {
        perror("Failed to receive response message");
        close(sockfd);
        return -1;
    }

    // Step 4: decode response message
    if (strcmp(buffer, "?JoinAccept") != 0) {
        printf("Join request denied by host\n");
        close(sockfd);
        return -1;
    }

    // Step 5: call @connectToRoomNetwork function to connect with the rest of room
    int result = connectToRoomNetwork(sockfd);
    if (result < 0) {
        perror("Failed to connect to room network");
        close(sockfd);
        return -1;
    }

    return sockfd;
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
    
    
    // Step 1: verify if @clientSocketFds is NULL, if yes => return -1
    if (clientSocketFds == NULL) {
        return -1;
    }
    
    // Step 2: verify if *clientSocketFds is NULL, if yes => allocate it as an array of @room->maxPlayer element
    if (*clientSocketFds == NULL) {
        *clientSocketFds = malloc(room->maxPlayer * sizeof(int));
        if (*clientSocketFds == NULL) {
            return -1;
        }
    }
    
    // Step 3: check if the current number of players of rooms (@room->currentNumber) is 2 or not?
    //      If yes, return 0 (2 means that the room contains only host and this player)
    if (room->currentNumber == 2) {
        return 0;
    }
    
    // Step 4: do a for loop to create new connections to all of the members of room
    //      except the first and the last one (because they are the host and this player)
    int i, fd;
    struct sockaddr_in servAddr;
    for (i = 1; i < room->currentNumber - 1; i++) {
        // Create a new socket
        fd = socket(AF_INET, SOCK_STREAM, 0);
        if (fd < 0) {
            return -1;
        }
        
        // Set the socket address
        memset(&servAddr, 0, sizeof(servAddr));
        servAddr.sin_family = AF_INET;
        servAddr.sin_addr.s_addr = inet_addr(room->players[i].ipAddr);
        servAddr.sin_port = htons(PORT);
        
        // Connect to the server
        if (connect(fd, (struct sockaddr*)&servAddr, sizeof(servAddr)) < 0) {
            close(fd);
            return -1;
        }
        
        // Write the new socket into *clientSocketFds
        (*clientSocketFds)[i] = fd;
    }
    
    return 0;

    


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

    // Step 1: encode room's in4 by calling the function @roomToStr from MSGCode module
    char *roomIn4 = roomToStr(&room);

    // Step 2: send the new encoding message to new player via @newPlayerSocketFd
    if (send(newPlayerSocketFd, roomIn4, strlen(roomIn4), 0) < 0) {
        perror("Failed to send room in4");
        return -1;
    }

    return 0;
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

