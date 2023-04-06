//
//  msg.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "msg.h"
#include "../../Support/Support.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>

// socket lib
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <unistd.h>

// threads lib
#include <pthread.h>

int sendToGame(int msgid, msg message) {
    message.msg_type = 3; // 3 indicate C to Python
    // msgsnd to send message
    if (msgsnd(msgid, &message, sizeof(message), 0) == -1) {
        write(1, "msgsnd failed\n", 14);
        return -1;
    }
    return 0;
}

int recvFromGame(int msgid, msg **message) {
    if (message == NULL) {
        return -1;
    } else if (*message == NULL) {
        *message = malloc(sizeof(msg));
    }
    
    (*message)->msg_type = 2; // 2 indicate Python to C

    // msgsnd to send message
    if (msgrcv(msgid, (*message), sizeof(**message), (*message)->msg_type, 0) == -1) {
        write(1, "msgrcv failed\n", 14);
        return -1;
    }

    return 0;
}

// The function @requestGameState is used to request the current game state from game (application layer) to send to the new player
// parameters: {
//  @msgid: used to identify message queue
//  @results: used to write the result of game state request from game
// }
// @return: 0 if successfully request or -1 if not
int requestGameState(int msgid, char** results) {
    // Step 1: Send the request to game via msgid
    //      The request has the form: "?GameState"
    // Step 2: Wait for the response from game
    // Step 3: Write into the results
    //      Step 3.1: if results is NULL => return -1
    //      Step 3.2: if *results is NULL => allocate *results
    //      Step 3.3: write the results into results

    // +++ YOUR CODE HERE +++ //
}

// The function @sendGameState is used to send the game state to update current game
// parameters: {
//  @msgid: used to identify message queue
//  @encodedGameState: the new game state used to update current game state
// }
int sendGameState(int msgid, char* encodedGameState) {
    
}


