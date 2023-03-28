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
#include <errno.h>
#include <ifaddrs.h>
#include <fcntl.h>
#include <net/if.h>

#include "Error/Error.h"
#include "Client/Client.h"
#include "Session/Session.h"
#include "IPC_Interface/Message/msg.h"
#include "MSGCode/MSGCode.h"

Client **clients = NULL;

#define BUFFLEN 1024
#define PORT 12345

// Max number of players - 1 (host)
#define MAX_PLAYER 12

void getMyIP(char *ip_addr) {
    
    struct ifaddrs *ifap, *ifa;
    struct sockaddr_in *sa;
    char *ip_address;

    getifaddrs(&ifap);
    for (ifa = ifap; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr->sa_family == AF_INET) {
            sa = (struct sockaddr_in *) ifa->ifa_addr;
            ip_address = inet_ntoa(sa->sin_addr);
            if (ifa->ifa_flags & IFF_UP && ifa->ifa_flags & IFF_RUNNING && ifa->ifa_addr->sa_family == AF_INET) {
                unsigned long ip_addr_length = strlen(ip_address);
                if (ip_addr == NULL) ip_addr = malloc(ip_addr_length+1);
                strncpy(ip_addr, ip_address, ip_addr_length);
                ip_addr[ip_addr_length] = '\0';
                freeifaddrs(ifap);
                return;
                
            }
        }
    }
}
 
int main(int argc, char **argv) {
    if (argc != 3) {
        write(1, "Number of arguments is not confortable\n", 39);
        exit(1);
    }
    
    // +++ argv[1] is the mode of program +++ //
    
    // ++ mode = 0 => create room ++ //
    // + ./main 0 roomName + //
    
    // ++ mode = 1 => join room ++ //
    // + ./main 0 hostip + //
    
    int mode = atoi(argv[1]);
    if (!mode) {
        write(1, "Invalid mode!\n", 14);
        exit(1);
    }
    
    if (mode == 1) {
        // mode = 1 => create new room
        if (argc != 3) {
            write(1, "Number of arguments is not confortable\n", 39);
            exit(1);
        }
        
        // Get my ip
        char *roomName = argv[2];
        char *my_ip_addr = malloc(16);
        getMyIP(my_ip_addr);
        
        // Get my username
        write(1, "What is your user name?\n> ", 26);
        int MAX_NAME_LENGTH = 64;
        char *myName = malloc(MAX_NAME_LENGTH+1);
        ssize_t myName_length = read(1, myName, MAX_NAME_LENGTH);
        myName[myName_length] = '\0';
        
        // Create my player
        Player me = initPlayer(my_ip_addr, myName);
        // create my room
        Room myRoom = createRoom(roomName, MAX_PLAYER, me);
        

        
        
        
        int opt = 1;
        // The main socket of this client
        clients = (Client**)malloc(MAX_PLAYER*sizeof(Client*));
        int master_socket;
        
        // Initialize all other players
        for (int i = 0; i<MAX_PLAYER; ++i) {
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
        
        if (listen(master_socket, MAX_PLAYER) < 0)
            stop("Error listening on master socket");
        
        write(1, "Waiting for connection ...\n", 27);
        
        while (1) // The main loop of program
        {
            //            // +++ receive from game +++ //
            //            msg message;
            //
            //            // +++ prepare message to send to another player +++ //
            //            int network_msg_length = sizeof(message.msg_text);
            //            char *network_msg = malloc(network_msg_length+1);
            //            strncpy(network_msg, message.msg_text, network_msg_length);
            //            network_msg[network_msg_length] = '\0';
            //
            //            if (recv_from_python(&message) < 0) {
            //                write(1, "ERROR receiving from Python\n", 28);
            //            }
            
            // Clear the socket set
            FD_ZERO(&readfds);
            
            // Add the master socket to socket set
            FD_SET(master_socket, &readfds);
            
            max_sd = master_socket;
            
            // Add all valid socket to socket set
            for (int i=0; i<MAX_PLAYER; ++i) {
                if (clients[i] == NULL) continue;
                sd = clients[i]->socket_fd;
                if (sd > 0) {
                    FD_SET(sd, &readfds);
                    
                    // If socket_fd is positive, then the client is valid
                    //                    send_msg(*clients[i], network_msg);
                }
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
                    buffer[valread] = '\0';
                    
                    write(1, buffer, strlen(buffer));
                    char *new_name = NULL;
                    // Decode destination message
                    if (strncmp(buffer, "username: ", 10) == 0) {
                        new_name = malloc(valread-10);
                        strncpy(new_name, buffer+10, valread-10);
                    }
                                        
                    // +++ Initialize new client +++ //
                    newClient = initClient(new_ip_addr, new_name, new_socket);
                    
                    // add client to the room
                    addPlayer(&myRoom, newClient.player);
                    
                    // Greeting message for joining the room
                    write(1, "Successfully connected!\n", 24);
                    
                    // Add the new socket to our player list
                    for (int i=0; i<MAX_PLAYER; ++i) {
                        if (clients[i] == NULL)
                        {
                            clients[i] = &newClient;
                            break;
                        }
                    }
                    
                    // Send the room information to the new player
                    char *room_in4 = malloc(4096);
                    roomToStr(myRoom, room_in4);
                    send_msg(newClient, room_in4);
                }
            } else {
                // If something happens on another socket => player send new signal
                for (int i=0; i<MAX_PLAYER; ++i) {
                    if (clients[i] == NULL) continue;
                    sd = clients[i]->socket_fd;
                    if (FD_ISSET(sd, &readfds)) {
                        char *buffer = malloc(1024);
                        msg message;
                        int val_recv;
                        if ((val_recv=recv_msg(*clients[i], buffer)) < 0) {
                            write(1, "cannot receive message from network\n", 36);
                            continue;
                        } else {
                            strncpy(message.msg_text, buffer, val_recv);
                            message.msg_text[val_recv] = '\0';
                            fputs(message.msg_text, stdout);
                            //                            send_to_python(message);
                        }
                        
                    }
                }
            }
        }
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    else {
        // mode = 2 => join room
        char *host_ip_addr = argv[2];
        
        // first socket, is used to connect to the room
        int first_socket;
        
        // The main socket that listen for all connect
        first_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (first_socket < 0) {
            perror("Error creating new socket");
            exit(1);
        }
        
        // room's host
        struct sockaddr_in host_addr;
        host_addr.sin_family = AF_INET;
        inet_pton(AF_INET, host_ip_addr, &(host_addr.sin_addr));
        host_addr.sin_port = htons(PORT);
        
        // Connect to the room
        write(1, "Waiting for connection to the room\n", 35);
        if (connect(first_socket, (struct sockaddr *)&host_addr, sizeof(host_addr)) < 0) {
            perror("ERROR connecting to room");
            exit(1);
        }
        write(1, "Successfully connected to the room\n", 35);
        
        // Get the username of user
        write(1, "> username: ", 12);
        char *username = malloc(65);
        ssize_t username_length = read(0, username, 64);
        username[username_length-1] = '\0';
                
        // send the first message: username
        char *usernameMSG = malloc(10+username_length);
        sprintf(usernameMSG, "username: %s", username);
        usernameMSG[10+username_length-1] = '\0';
        
        
        
        if (send(first_socket, usernameMSG, 10+username_length-1, 0) != 10+username_length-1) {
            perror("ERROR sending username");
            exit(1);
        }
        
        // receive the first message about room in4
        char *room_in4 = malloc(4096);
        ssize_t val_recv = recv(first_socket, room_in4, 4095, 0);
        
        Room myRoom;
        if (val_recv < 0) {
            perror("ERROR receiving room in4");
            exit(1);
        } else {
            room_in4[val_recv] = '\0';
//            strToRoom(room_in4, &myRoom);
            fputs(room_in4, stdout);
        }
        
        
        
        
        
        
        // +++++++++++++++++++++++++++++++++++++++++++++++++= //
        
        int opt = 1;
        // The main socket of this client
        clients = (Client**)malloc(MAX_PLAYER*sizeof(Client*));
        int master_socket;
        
        // Initialize all other players
        for (int i = 0; i<MAX_PLAYER; ++i) {
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
        
        if (listen(master_socket, MAX_PLAYER) < 0)
            stop("Error listening on master socket");
        
        write(1, "Waiting for connection ...\n", 27);
        
        while (1) // The main loop of program
        {
            //            // +++ receive from game +++ //
            //            msg message;
            //
            //            // +++ prepare message to send to another player +++ //
            //            int network_msg_length = sizeof(message.msg_text);
            //            char *network_msg = malloc(network_msg_length+1);
            //            strncpy(network_msg, message.msg_text, network_msg_length);
            //            network_msg[network_msg_length] = '\0';
            //
            //            if (recv_from_python(&message) < 0) {
            //                write(1, "ERROR receiving from Python\n", 28);
            //            }
            
            // Clear the socket set
            FD_ZERO(&readfds);
            
            // Add the master socket to socket set
            FD_SET(master_socket, &readfds);
            
            max_sd = master_socket;
            
            // Add all valid socket to socket set
            for (int i=0; i<MAX_PLAYER; ++i) {
                if (clients[i] == NULL) continue;
                sd = clients[i]->socket_fd;
                if (sd > 0) {
                    FD_SET(sd, &readfds);
                    
                    // If socket_fd is positive, then the client is valid
                    //                    send_msg(*clients[i], network_msg);
                }
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
                    for (int i=0; i<MAX_PLAYER; ++i) {
                        if (clients[i] == NULL)
                        {
                            clients[i] = malloc(sizeof(Client));
                            clients[i] = &newClient;
                            break;
                        }
                    }
                    
                    // Send the room information to the new player
                    send_msg(newClient, "Hello WORLD!\0");
                }
            } else {
                // If something happens on another socket => player send new signal
                for (int i=0; i<MAX_PLAYER; ++i) {
                    if (clients[i] == NULL) continue;
                    sd = clients[i]->socket_fd;
                    if (FD_ISSET(sd, &readfds)) {
                        char *buffer = malloc(1024);
                        msg message;
                        int val_recv;
                        if ((val_recv=recv_msg(*clients[i], buffer)) < 0) {
                            write(1, "cannot receive message from network\n", 36);
                            continue;
                        } else {
                            strncpy(message.msg_text, buffer, val_recv);
                            message.msg_text[val_recv] = '\0';
                            fputs(message.msg_text, stdout);
//                            send_to_python(message);
                        }
                        
                    }
                }
            }
        }
    }
}

