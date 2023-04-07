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
#include <pthread.h>

#include "Support/Support.h"
#include "../Session/Session/Room.h"
#include "IPC_Interface/Message/msg.h"
#include "MSGCode/MSGCode.h"

int *clientFds = NULL;

#define BUFFLEN 1024
#define PORT 12345

// Max number of players - 1 (host)
#define MAX_PLAYER 12

struct argv {
    int mode;
    char *roomName;
    char *myName;
};


void *bindNewDiscoveringThread(void *arg) {
    // The socket used for host of a room to listen if someone need to discover room
    char *roomName = (char *)arg;
    int hostSocket = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in hostAddr;
    memset(&hostAddr, 0, sizeof(hostAddr));
    hostAddr.sin_family = AF_INET;
    hostAddr.sin_addr.s_addr = INADDR_ANY;
    hostAddr.sin_port = htons(12345);
    
    int host_len = sizeof(hostAddr);
    
    if (bind(hostSocket, (const struct sockaddr *)(&hostAddr), sizeof(hostAddr)) < 0)
        stop("Error binding on master socket");
    
    char *buffer = malloc(64);
    if (recvfrom(hostSocket, buffer, 63, 0, (struct sockaddr *)&hostAddr, (socklen_t *)&host_len) <0) {
        int fd = open("/Users/duy/Desktop/demo.log", O_RDWR | O_APPEND);
        write(fd, "Failed received", strlen("Failed received"));
        write(fd, "\n", 1);
        close(fd);
    } else {
        int fd = open("/Users/duy/Desktop/demo.log", O_RDWR | O_APPEND);
        write(fd, "Successfully received", strlen("Successfully received"));
        write(fd, "\n", 1);
        close(fd);
    }
    if (strncmp(buffer, "?DiscoverRoom", 13) == 0) {
        char *message = malloc(64);
        sprintf(message, "!Active %s", roomName);
        hostAddr.sin_port = htons(54321);
        sendto(hostSocket, message, strlen(message), 0, (struct sockaddr *)&hostAddr, (socklen_t)host_len);
    }
    return NULL;
}

void *mainThread(void *argv) {
    
    int mode = ((struct argv *)argv)->mode;
    char *roomName = ((struct argv *)argv)->roomName;
    char *myName = ((struct argv *)argv)->myName;
    
    // Get my ip
    char *my_ip_addr = malloc(16);
    my_ip_addr[15] = '\0';
    getMyIP(my_ip_addr);


    // Create my player
    Player me = initPlayer(my_ip_addr, myName);
    // create my room
    Room myRoom = createRoom(roomName, MAX_PLAYER, me);

    int opt = 1;
    // The main socket of this client
    int master_socket;

    // Initialize all other players
    for (int i = 0; i < myRoom.maxPlayer; ++i) {
        clientFds[i] = -1;
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
    else
        clientFds[0] = master_socket;

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
        //            if (recvFromGame(&message) < 0) {
        //                write(1, "ERROR receiving from Python\n", 28);
        //            }

        // Clear the socket set
        FD_ZERO(&readfds);

        max_sd = -1;

        // Add all valid socket to socket set
        for (int i = 0; i < MAX_PLAYER; ++i)
        {
            if (clientFds[i] == -1)
                continue;
            sd = clientFds[i];
            if (sd > 0)
            {
                FD_SET(sd, &readfds);

                // If socket_fd is positive, then the client is valid
                //                    send_msg(*clients[i], network_msg);
            }
            if (sd > max_sd)
                max_sd = sd;
        }

        activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);
        if ((activity < 0) && (errno != EINTR))
            write(1, "Select error\n", 13);
        
        if (FD_ISSET(master_socket, &readfds))
        {
            // If something is gone in master socket => new client request to connect
            if ((new_socket = accept(master_socket, (struct sockaddr *)(&address), (socklen_t *)&addrlen)) < 0)
            {
                perror("Error connecting");
                continue;
            }
            else
            {

                // +++ Get the IP of new connection +++ //
                char *new_ip_addr = malloc(INET_ADDRSTRLEN);
                inet_ntop(AF_INET, &(address.sin_addr), new_ip_addr, INET_ADDRSTRLEN);

                // +++ Get the username of new connection +++ //
                // Read the destination message
                memset(buffer, 0, BUFFLEN);
                valread = recv(new_socket, buffer, BUFFLEN - 1, 0);
                buffer[valread] = '\0';

                char *new_name = NULL;
                // Decode destination message
                if (strncmp(buffer, "username: ", 10) == 0)
                {
                    new_name = malloc(valread - 10);
                    strncpy(new_name, buffer + 10, valread - 10);
                }

                // +++ Initialize new player +++ //
                Player newPlayer = initPlayer(new_ip_addr, new_name);

                // add player to the room
                addPlayer(&myRoom, &newPlayer);

                // Greeting message for joining the room
                write(1, "Successfully connected!\n", 24);

                // Add the new socket to our player list
                for (int i = 0; i < MAX_PLAYER; ++i)
                {
                    if (clientFds[i] == -1)
                    {
                        clientFds[i] = new_socket;
                        break;
                    }
                }

                // Send the room information to the new player
                char *room_in4 = malloc(4096);
                roomToStr(myRoom, room_in4);
                send(new_socket, room_in4, strlen(room_in4), 0);
            }
        }
        else
        {
            // If something happens on another socket => player send new signal
            for (int i = 0; i < MAX_PLAYER; ++i)
            {
                if (clientFds[i] == -1)
                    continue;
                sd = clientFds[i];
                if (FD_ISSET(sd, &readfds))
                {
                    // char *buffer = malloc(1024);
                    // if ((valread = recv(sd, buffer, 1023, 0)) == 0) {
                    //     perror("ERROR reading");
                    //     exit(EXIT_FAILURE);
                    // }
                    // buffer[valread] = '\0';
                    // fputs(buffer, stdout);
                    // msg message;
                    // int val_recv;
                }
            }
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    clientFds = (int*)malloc(MAX_PLAYER * sizeof(int));

    // +++ argv[1] is the mode of program +++ //
    // +++ argv[2] is the room name +++ //
    // +++ argv[3] is the player name +++ //

    // ++ mode = 1 => create room ++ //
    // + ./main 1 roomName playerName + //

    // ++ mode = 2 => join room ++ //
    // + ./main 2 roomName playerName + //

    if (argc != 4) {
        write(1, "Number of arguments is not confortable\n", 39);
        exit(1);
    }

    int mode = atoi(argv[1]);
    if (!mode) {
        write(1, "Invalid mode!\n", 14);
        exit(1);
    }

    struct argv myarg;
    myarg.mode = mode;
    myarg.roomName = argv[2];
    myarg.myName = argv[3];


    if (mode == 1) {
        // mode = 1 => create new room
        pthread_t roomDiscoverTid, mainTid;
        pthread_create(&roomDiscoverTid, NULL, bindNewDiscoveringThread, argv[2]);
        pthread_create(&mainTid, NULL, mainThread, &myarg);
        
        pthread_join(roomDiscoverTid, NULL);
        pthread_join(mainTid, NULL);
        
        return 0;
        
    }

    else
    {
        // mode = 2 => join room
        char *host_ip_addr = argv[2];
        // resolveRoomToIP(roomName, &host_ip_addr);

        // first socket, is used to connect to the room
        int first_socket;

        // The main socket that listen for all connect
        first_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (first_socket < 0)
        {
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
        if (connect(first_socket, (struct sockaddr *)&host_addr, sizeof(host_addr)) < 0)
        {
            perror("ERROR connecting to room");
            exit(1);
        }
        write(1, "Successfully connected to the room\n", 35);

        // Get the username of user
        char *username = argv[3];
        unsigned long username_length = strlen(username);

        // send the first message: username
        unsigned long msgLength = 10 + username_length;
        char *usernameMSG = malloc(msgLength+1);
        sprintf(usernameMSG, "username: %s", username);
        usernameMSG[msgLength] = '\0';

        if (send(first_socket, usernameMSG, msgLength, 0) != msgLength)
        {
            perror("ERROR sending username");
            exit(1);
        }

        // receive the first message about room in4
        char *room_in4 = malloc(4096);
        ssize_t val_recv = recv(first_socket, room_in4, 4095, 0);

        Room myRoom;
        if (val_recv < 0)
        {
            perror("ERROR receiving room in4");
            exit(1);
        }
        else
        {
            room_in4[val_recv] = '\0';
            write(1, room_in4, strlen(room_in4));
//            strToRoom(room_in4, &myRoom);
            // connectToRoomNetwork(myRoom, &clientFds);
        }

        char **hostIPs = NULL;
        char **roomNames = NULL;
//        discorverRoom(&hostIPs, &roomNames);
//        fputs(hostIPs[0], stdout);
//        int sock = socket(AF_INET, SOCK_DGRAM, 0);
//        struct sockaddr_in servaddr;
//        memset(&servaddr, 0, sizeof(servaddr));
//        servaddr.sin_family = AF_INET;
//        servaddr.sin_addr.s_addr = inet_addr("172.20.10.6");
//        servaddr.sin_port = htons(12345);
//        char* message = "?DiscoverRoom\0";
//        if (sendto(sock, message, strlen(message), 0, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
//            perror("Failed sending broadcast message");
//            close(sock);
//            return -1;
//        } else {
//            fputs("Successfully sent\n", stdout);
//        }
//        char *buffer_1 = malloc(64);
//        socklen_t servaddr_length = sizeof(servaddr);
//        if (recvfrom(sock, buffer_1, 63, 0, (struct sockaddr *)&servaddr, &servaddr_length) < 0) {
//            return -1;
//        } else {
//            fputs(buffer_1, stdout);
//        }

        return 0;

        // ++++++++++++++++++++++++++++++++++++++++++++++++++ //

        int opt = 1;
        // The main socket of this client

        int master_socket;

        // Initialize all other players
        for (int i = 0; i < MAX_PLAYER; ++i)
        {
            clientFds[i] = -1;
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
            //            if (recvFromGame(&message) < 0) {
            //                write(1, "ERROR receiving from Python\n", 28);
            //            }

            // Clear the socket set
            FD_ZERO(&readfds);

            // Add the master socket to socket set
            FD_SET(master_socket, &readfds);

            max_sd = master_socket;

            // Add all valid socket to socket set
            for (int i = 0; i < MAX_PLAYER; ++i)
            {
                if (clientFds[i] == -1)
                    continue;
                sd = clientFds[i];
                if (sd > 0)
                {
                    FD_SET(sd, &readfds);

                    // If socket_fd is positive, then the client is valid
                    //                    send_msg(*clients[i], network_msg);
                }
                if (sd > max_sd)
                    max_sd = sd;
            }

            activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);
            if ((activity < 0) && (errno != EINTR))
                write(1, "Select error\n", 13);

            if (FD_ISSET(master_socket, &readfds))
            {
                // If something is gone in master socket => new client request to connect
                if ((new_socket = accept(master_socket, (struct sockaddr *)(&address), (socklen_t *)&addrlen)) < 0) {
                    perror("Error connecting");
                    continue;
                }
                else {
                    // +++ Get the IP of new connection +++ //
                    char *new_ip_addr = malloc(INET_ADDRSTRLEN);
                    inet_ntop(AF_INET, &(address.sin_addr), new_ip_addr, INET_ADDRSTRLEN);

                    // +++ Get the username of new connection +++ //
                    // Read the destination message
                    memset(buffer, 0, BUFFLEN);
                    valread = recv(new_socket, buffer, BUFFLEN - 1, 0);
                    buffer[valread - 2] = '\0';
                    char *new_name = NULL;
                    // Decode destination message
                    if (strncmp(buffer, "username: ", 10) == 0)
                    {
                        new_name = malloc(valread - 10);
                        strncpy(new_name, buffer + 10, valread - 10);
                    }

                    // +++ Initialize new client +++ //
                    Player newPlayer = initPlayer(new_ip_addr, new_name);

                    // Greeting message for joining the room
                    write(1, "Successfully connected!\n", 24);

                    // Add the new socket to our player list
                    for (int i = 0; i < MAX_PLAYER; ++i)
                    {
                        if (clientFds[i] == -1)
                        {
                            clientFds[i] = new_socket;
                            break;
                        }
                    }

                    // Send the room information to the new player
                }
            }
            else
            {
                // If something happens on another socket => player send new signal
                for (int i = 0; i < MAX_PLAYER; ++i)
                {
                    if (clientFds[i] == -1)
                        continue;
                    sd = clientFds[i];
                    if (FD_ISSET(sd, &readfds))
                    {
                        char *buffer = malloc(1024);
                        msg message;
                        int val_recv;
                        if ((val_recv = recv(clientFds[i], buffer, 1023, 0)) < 0)
                        {
                            write(1, "cannot receive message from network\n", 36);
                            continue;
                        }
                        else
                        {
                            strncpy(message.msg_text, buffer, val_recv);
                            message.msg_text[val_recv] = '\0';
                            fputs(message.msg_text, stdout);
                            //                            sendToGame(message);
                        }
                    }
                }
            }
        }
    }
}
