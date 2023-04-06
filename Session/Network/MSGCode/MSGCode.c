//
//  MSGCode.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "MSGCode.h"
#include "../Support/Support.h"

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

int roomToStr(Room room, char *buffer) {
    // Total length of encoding message
    int encoded_msg_length = 0;
    
    // encoding message
    char *encodingStr = malloc(4096);
    
    sprintf(encodingStr, "name: %s\nmaxPlayer: %d\ncurrentNumber: %d\n", room.name, room.maxPlayer, room.currentNumber);
    encoded_msg_length += strlen(encodingStr);

    for (int i=0; i<room.maxPlayer; i++) {
        if (isNA(room.players[i])) break;
        
        // length of in4 of each player in room
        unsigned long player_in4_length = 11+strlen(room.players[i].ipAddr)+strlen(room.players[i].name);

        char *player_in4 = malloc(player_in4_length+1);
        sprintf(player_in4, "player: %s, %s", room.players[i].ipAddr, room.players[i].name);
        player_in4[player_in4_length] = '\0';
        
        // add to encoding message
        strncat(encodingStr, player_in4, strlen(player_in4));

        encoded_msg_length += player_in4_length;

    }
    encodingStr[encoded_msg_length] = '\0';
    
    if (buffer == NULL) {
        buffer = malloc(4096);
    }
    strncpy(buffer, encodingStr, encoded_msg_length);
    buffer[encoded_msg_length] = '\0';
    return 0;
}

int strToRoom(char *buffer, Room *room) {
    if (buffer == NULL) {
        write(1, "String is NULL\n", 15);
        return -1;
    }
    
    int count = 0; // variable to track the iteration of token
    
    char **decodingData;
    
    int num_token = split(buffer, "\n", &decodingData);
    for (int i=0; i<num_token; ++i) {
        char *token = decodingData[i];
        if (strncmp(token, "name: ", 6) == 0) {
            // Regconize room name
            unsigned long name_length = strlen(token+6);
            room->name = token+6;
            (room->name)[name_length] = '\0';
        } else if (strncmp(token, "maxPlayer: ", 11) == 0) {
            // Regconize room max number of players
            int maxPlayer = atoi(token+11);
            if (maxPlayer == 0) {
                // Handle error
                // But so tired now
                // Let it here for another day
                return -1;
            } else {
                room->maxPlayer = maxPlayer;
            }
        } else if (strncmp(token, "currentNumber: ", 15) == 0) {
            int currentNumber = atoi(token+15);
            if (currentNumber == 0) {
                // Handle if there is error
                return -1;
            } else {
                room->currentNumber = currentNumber;
            }
        } else {
            // Regconize room players
            if (room->players == NULL) {
                room->players = malloc(room->maxPlayer);
            }
            
            char *rest = token+8;
            
            char **result = NULL;
            split(rest, ", ", &result);

            room->players[count-3].ipAddr = result[0];
            room->players[count-3].name = result[1];
            
        }

        count += 1;
        token = strtok(NULL, "\n");
    }
    
    return 0;
}
