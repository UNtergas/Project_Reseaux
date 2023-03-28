//
//  msg.c
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#include "msg.h"
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

int send_to_python(msg message) {
    int msgid = msgget(MSG_KEY, 0666 | IPC_CREAT);
    message.msg_type = 3; // 3 indicate C to Python
    // msgsnd to send message
    if (msgsnd(msgid, &message, sizeof(message), 0) == -1) {
        write(1, "msgsnd failed\n", 14);
        return -1;
    }
    return 0;
}

int recv_from_python(msg *message) {
    if (message == NULL) {
        message = malloc(sizeof(msg));
    }
    int msgid = msgget(MSG_KEY, 0666 | IPC_CREAT);
    
    message->msg_type = 2; // 2 indicate Python to C

    // msgsnd to send message
    if (msgrcv(msgid, message, sizeof(*message), message->msg_type, 0) == -1) {
        write(1, "msgrcv failed\n", 14);
        return -1;
    }

    return 0;
}
