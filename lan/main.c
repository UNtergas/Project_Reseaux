//
//  main.c
//  internet_project
//
//  Created by Pham Duy on 27/03/2023.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/select.h>
#include "Error/Error.h"
#include <errno.h>
#include "Client/Client.h"
#include "Message/msg.h"

Client **clients = NULL;

#define BUFFLEN 1024

// Max number of players - 1 (host)
#define N 12

int main(int argc, char **argv)
{
    // Handle process
    if (argc != 4) {
        write(1, "Number of arguments is not confortable\n", 39);
        exit(1);
    }

    // argv[1] is ip addresss
    char *ip_addr = argv[1];

    // argv[2] is the port
    int PORT = atoi(argv[2]);

    // check if the port is possible
    if (!PORT) {
        write(1, "Invalid port!\n", 14);
        exit(1);
    }

    int opt = 1;
    // The main socket of this client
    clients = (Client**)malloc(N*sizeof(Client*));
    int master_socket;
    
    // Initialize all other players
    for (int i = 0; i<N; ++i) {
        clients[i] = NULL;
    }
    int max_sd, sd, activity, new_socket, addrlen;
    ssize_t valread;

    // buffer for user
    char buffer[BUFFLEN];
    memset(buffer, 0, BUFFLEN);

    fd_set readfds;

    // The main socket that listen for all connect
    master_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (master_socket < 0)
        stop("Error creating new socket");

    if (setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)(&opt), sizeof(opt)) < 0)
        perror("Error setting socket option");

    // Sockaddr_in structure
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(master_socket, (const struct sockaddr *)(&address), sizeof(address)) < 0)
        stop("Error binding on master socket");

    if (listen(master_socket, N) < 0)
        stop("Error listening on master socket");

    write(1, "Waiting for connection ...\n", 27);

    int pid = fork();
    
    if (pid == 0) {
        // Process connection in the network
        while (1) // The main loop of program
        {
            // Clear the socket set
            FD_ZERO(&readfds);

            // Add the master socket to socket set
            FD_SET(master_socket, &readfds);
            
            max_sd = master_socket;

            // Add all valid socket to socket set
            for (int i=0; i<N; ++i) {
                sd = clients[i]->socket_fd;
                if (sd > 0) FD_SET(sd, &readfds);
                if (sd > max_sd) max_sd = sd;
            }

            activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);
            if ((activity < 0) && (errno != EINTR))
                write(1, "Select error\n", 13);

            
            if (FD_ISSET(master_socket, &readfds)) {
                // If something is gone in master socket => new client request to connect
                if ((new_socket = accept(master_socket, (struct sockaddr *)(&address), (socklen_t*)&addrlen)) < 0) {
                    perror("Error connecting");
                    continue;
                } else {
                    Client newClient;
                    
                    // +++ Get the IP of new connection +++ //
                    char *new_ip_addr = malloc(INET_ADDRSTRLEN);
                    inet_ntop(AF_INET, &(address.sin_addr), new_ip_addr, INET_ADDRSTRLEN);
                    
                    // +++ Get the username of new connection +++ //
                    // Read the destination message
                    memset(buffer, 0, BUFFLEN);
                    valread = recv(new_socket, buffer, BUFFLEN-1, 0);
                    buffer[valread - 2] = '\0';
                    char *new_name = NULL;
                    // Decode destination message
                    if (strncmp(buffer, "username: ", 10) == 0) {
                        new_name = malloc(valread-10);
                        strncpy(new_name, buffer+10, valread-10);
                    }
                    
                    // +++ Initialize new client +++ //
                    newClient = initClient(new_ip_addr, new_name, new_socket);
                    
                    // Greeting message for joining the room
                    write(1, "Successfully connected!\n", 24);
                    
                    // Add the new socket to our player list
                    for (int i=0; i<N; ++i) {
                        if (clients[i] == NULL)
                        {
                            clients[i] = malloc(sizeof(Client));
                            clients[i] = &newClient;
                            break;
                        }
                    }
                    
                    // Send the room information to the new player
                }
            } else {
                // If something happens on another socket => player send new signal
            }
        }
    } else {
        // Process the ouput to the network
        while (1) {
            msg *message = malloc(sizeof(msg));
            if (recv_from_python(message) < 0) {
                write(1, "cannot receive message from game\n", 33);
                continue;
            }
            
            
        }
    }
    
    
    while (1)
    {
        // Clear the socket set
        FD_ZERO(&readfds);

        // Add the master socket to socket set
        FD_SET(master_socket, &readfds);
        
        max_sd = master_socket;

        // Add all valid socket to socket set
        for (int i=0; i<N; ++i) {
            sd = clients[i]->socket_fd;
            if (sd > 0) FD_SET(sd, &readfds);
            if (sd > max_sd) max_sd = sd;
        }

        activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);
        if ((activity < 0) && (errno != EINTR))
            write(1, "Select error\n", 13);

        
        if (FD_ISSET(master_socket, &readfds)) {
            // If something is gone in master socket => new client request to connect
            if ((new_socket = accept(master_socket, (struct sockaddr *)(&address), (socklen_t*)&addrlen)) < 0) {
                perror("Error connecting");
                continue;
            } else {
                Client newClient;
                
                // +++ Get the IP of new connection +++ //
                char *new_ip_addr = malloc(INET_ADDRSTRLEN);
                inet_ntop(AF_INET, &(address.sin_addr), new_ip_addr, INET_ADDRSTRLEN);
                
                // +++ Get the username of new connection +++ //
                // Read the destination message
                memset(buffer, 0, BUFFLEN);
                valread = recv(new_socket, buffer, BUFFLEN-1, 0);
                buffer[valread - 2] = '\0';
                char *new_name = NULL;
                // Decode destination message
                if (strncmp(buffer, "username: ", 10) == 0) {
                    new_name = malloc(valread-10);
                    strncpy(new_name, buffer+10, valread-10);
                }
                
                // +++ Initialize new client +++ //
                newClient = initClient(new_ip_addr, new_name, new_socket);
                
                // Greeting message for joining the room
                write(1, "Successfully connected!\n", 24);
                
                // Add the new socket to our player list
                for (int i=0; i<N; ++i) {
                    if (clients[i] == NULL)
                    {
                        clients[i] = malloc(sizeof(Client));
                        clients[i] = &newClient;
                        break;
                    }
                }
                
                // Send the room information to the new player
            }
        } else {
            // If something happens on another socket => player send new signal
        }
    }
}

