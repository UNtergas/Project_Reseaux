//
//  MSGCode.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "MSGCode.h"
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
    
    sprintf(encodingStr, "name: %s\nmaxPlayer: %d\n", room.name, room.maxPlayer);
    encoded_msg_length += 19 + strlen(room.name) + 1;

    for (int i=0; i<room.maxPlayer; i++) {
        if (isNA(room.players[i])) break;
        
        // length of in4 of each player in room
        unsigned long player_in4_length = 11+strlen(room.players[i].ip_addr)+strlen(room.players[i].name);

        char *player_in4 = malloc(player_in4_length+1);
        sprintf(player_in4, "player: %s, %s", room.players[i].ip_addr, room.players[i].name);
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
    
    char *token;
    token = strtok(buffer, "\n");
    
    int count = 0; // variable to track the iteration of token
    
    while (token != NULL) {
        
        
        if (strncmp(token, "name: ", 6) == 0) {
            // Regconize room name
            unsigned long name_length = strlen(token+6);
            
            

            
//            if (room->name == NULL) {
//                room->name = malloc(name_length+1);
//            }
//            strncpy(room->name, token+6, name_length-3);
            room->name = token+6;
            (room->name)[name_length] = '\0';
            int fd = open("/Users/duy/Desktop/Learn_university/annee_3/Semetre 6/internet_project/internet_project/internet_project/demo.log", O_WRONLY | O_APPEND);
            write(fd, room->name, name_length);
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
        } else {
            // Regconize room players
            char *player_in4_token = strtok(token+8, ", ");
            strncpy(room->players[count-2].ip_addr, player_in4_token, strlen(player_in4_token));
            
            player_in4_token = strtok(NULL, ", ");
            strncpy(room->players[count-2].name, player_in4_token, strlen(player_in4_token));
        }

        
        count += 1;
        token = strtok(NULL, "\n");
        
    }
    return 0;
}
