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



typedef struct
{
    long msg_type; // identifier of message in kernel
    char msg_text[1024]; // content of message
} msg;

void setup_connection(int *my_fd, struct sockaddr_in *address);

int recv_from_python(msg *message);
int send_to_python(msg message);

#endif /* msg_h */
