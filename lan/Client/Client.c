#include "Client.h"
#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <strings.h>
#include <ifaddrs.h>

Client initClient(char *ip_addr, char *name, int socket_fd) {
    Player newPlayer = initPlayer(ip_addr, name);
    Client newClient = {NULL, socket_fd};
    newClient.player = malloc(sizeof(Player));
    copyPlayer(newClient.player, &newPlayer);
    return newClient;
}

int send_msg(Client client ,char* data) {
    unsigned long msg_length = strlen(data); // length of the message
    if (send(client.socket_fd, data, msg_length, 0) < 0) {
        fprintf(stderr, "Error sending data\n");
        return -1;
    }
    return 0;
}

int recv_msg(Client client, char* buffer) {
    unsigned long bytes_received = recv(client.socket_fd, buffer, 1024-1, 0);
    buffer[bytes_received] = '\0';
    if (bytes_received == -1) {
        fprintf(stderr, "Error receiving data\n");
        return -1;
    }
    return 0;
}

