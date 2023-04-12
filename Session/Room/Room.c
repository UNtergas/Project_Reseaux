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

#include "../../Network/IPC_Interface/Message/msg.h"

int isFull(Room room)
{
    if (room.maxPlayer == room.currentNumber)
        return 1;
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
int destroyRoom(Room *room)
{
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
int joinRoom(char *hostIPaddr, char *roomName)
{
    // Step 1: connect with host via @hostIPaddr (using TCP socket)
    // Step 2: send the joining request message
    //      The message's content: ?Join{@roomName}
    //      replace the {@roomName} with @roomName
    // Step 3: wait for response
    // Step 4: decode response message
    // Step 5: call @connectToRoomNetwork function to connect with the rest of room

}
// The function @connectToRoomNetwork is used to connect to the rest of room (except host)
// The purpose is create a P2P network in room
// @parameters: {
//  @room: the room we want to connect to create a P2P network
//  @clientSocketFds: the list of used to write the new sockets we will create into
// }
int connectToRoomNetwork(Room room, int *clientSocketFds) {
    // Step 1: verify if @clientSocketFds is NULL, if yes => return -1
    // Step 2: verify if *clientSocketFds is NULL, if yes => allocate it as an array of @room.maxPlayer element
    // Step 3: check if the current number of players of rooms (@room.currentNumber) is 2 or not?
    //      If yes, return 0 (2 means that the room contains only host and this players)
    // Step 4: do a for loop to create new connections to all of the members of room
    //      except the first and the last one (because they are the host and this player)
    // Step 5: write new created socket into *clientSocketFds
    if (clientSocketFds == NULL) return -1;

    for (int i=2; i<room.currentNumber; ++i) { // the first person is exclusive cuz he is host, 2 is me
        if (isNA(room.players[i])) break;
        int newSocketFd = socket(AF_INET, SOCK_STREAM, 0);
        if (newSocketFd < 0) return -1;
        // room's host
        struct sockaddr_in player_addr;
        player_addr.sin_family = AF_INET;
        inet_pton(AF_INET, room.players[i].ipAddr, &(player_addr.sin_addr));
        player_addr.sin_port = htons(12345);

        if (connect(newSocketFd, (const struct sockaddr *)&player_addr, sizeof(player_addr)) < 0) return -1;
        else {
            for (int j=0; j<room.maxPlayer+1; ++j) {
                if (clientSocketFds[j] == -1) clientSocketFds[j] = newSocketFd;
            }
        }
    }
}
    
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

void addPlayer(Room *room, Player *newPlayer)
{
    if (isFull(*room))
        return;
    if (room->players == NULL)
    {
        room->players = malloc((room->maxPlayer) * sizeof(Player));
    }
    for (int i = 0; i < room->maxPlayer; ++i)
    {
        if (isNA(room->players[i]))
        {
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
int sendGameStateToNewPlayer(char *filePath, int newPlayerSocketFd) {
    // Open log
    int log_fd = open("/home/john/Desktop/demo.log", O_RDWR | O_APPEND | O_CREAT);
    int fd = open(filePath, O_RDONLY);

    char *buffer = malloc(369369);
    memset(buffer, 0, 369369);

    int valread = 0;
    do {
        if ((valread = read(fd, buffer, 369368)) < 0) {
            free(buffer);
            close(log_fd);
            close(fd);
            return -1;
        } else {
            write(log_fd, buffer, valread);
            write(log_fd, '\n', 1);
            close(log_fd);
            if (send(newPlayerSocketFd, buffer, valread, 0) < 0) {
                
                close(fd);
                free(buffer);
                return -1;
            } 
        }
    }
    while (buffer[valread] != EOF);

    free(buffer);
    close(fd);

    return 0;
}

int receiveFirstGameState(char *filePath, int hostSocketFd) {
    // receive file data and write to file
    int fd = open(filePath, O_RDWR | O_CREAT); 

    if (fd <= 0) return -1;

    char *buffer = malloc(369369);
    memset(buffer, 0, 369369);

    int log_fd = open("/home/parallels/Desktop/demo.log", O_RDWR | O_APPEND | O_CREAT);
    int valread = 0;
    do {
        valread = recv(hostSocketFd, buffer, sizeof(buffer), 0);
        if (valread < 0) {
            fclose(fd);
            free(buffer);
            return -1;
        } else if (valread == 0) {
            fclose(fd);
            free(buffer);
            return 0;   
        } else {
            write(log_fd, buffer, valread);
            fclose(log_fd);
            write(fd, buffer, valread);

        }
        int valread = recv(hostSocketFd, buffer, sizeof(buffer), 0);
    } 
    while (buffer[valread] != EOF);
    fclose(fd);
    free(buffer);  
    
    return 0;
}

int requestGameState(int mySocket)
{
    // Step 1: Send the request to game via msgid
    //      The request has the form: "?GameState"
    // Step 2: Wait for the response from game
    // Step 3: Write into the results
    //      Step 3.1: if results is NULL => return -1
    //      Step 3.2: if *results is NULL => allocate *results
    //      Step 3.3: write the results into results

    char* message = "PRE:{\"type\":\"save\",\"temp\": \"\",\"timestamp\":0}:POST\0";
    if (send(mySocket, message, strlen(message), 0) < 0) {
        return -1;
    }
    char *response = malloc(10);
    int valread;
    if ((valread = recv(mySocket, response, 9, 0)) < 0) {
        return -1;
    } else {
        response[valread] = '\0';
        if (strncmp(response, "!Done", 5) == 0) {
            return 0;
        }
    }
}