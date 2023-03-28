#ifndef CLIENT_H
#define CLIENT_H

#include "../Player/Player.h"
#include <netinet/in.h>
#include <arpa/inet.h>




typedef struct {
    Player *player;
    int socket_fd; // The socket
} Client;

extern Client **clients;

Client initClient(char *ip_addr, char *name, int socket_fd);

int send_msg(Client client, char *msg);
int recv_msg(Client client, char *msg);


#endif
