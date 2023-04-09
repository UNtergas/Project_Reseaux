//
//  msg.h
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#ifndef msg_h
#define msg_h

#include <stdio.h>

#define MSG_KEY 190234
#define C_TO_PY 2
#define PY_TO_C 3

typedef struct
{
    long msg_type;       // identifier of message in kernel
    char msg_text[1024]; // content of message
} msg;

int recvFromGame(int msgid, msg **message);
int sendToGame(int msgid, msg message);

int sendGameState(int msgid, char *encodedGameState);

#endif /* msg_h */
