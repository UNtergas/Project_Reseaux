//
//  getAvailableRoom.c
//  internet_project
//
//  Created by Pham Duy on 07/04/2023.
//

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
#include <sys/time.h>
#include <pthread.h>

#include "Network/Support/Support.h"

#define MAX_ROOMS 100

// ++++++++++++++++++++++++++++++++++++++++++++ Discover Room ++++++++++++++++++++++++++++++++++++++++++++ //
void *sendDiscoveringMessageThread(void *arg) {
    char *base_ip = (char *)arg;
    
    char* message = "?DiscoverRoom\0";
    
    // Iterate through all IP addresses in the LAN
    char* ip = (char*)malloc(INET_ADDRSTRLEN * sizeof(char));
    char buffer[64]; // Buffer for receiving message from active server
    struct sockaddr_in sa;
    
    // Send discovering message to all ip adress
    for (int i = 1; i<50; i++) {
        snprintf(ip, INET_ADDRSTRLEN, "%s%d", base_ip, i);

        // Convert the IP to binary
        inet_pton(AF_INET, ip, &(sa.sin_addr));

        // Do something with the IP here, like send a packet
        // Create a UDP socket for broadcasting
        int sock = socket(AF_INET, SOCK_DGRAM, 0);
        if (sock < 0) {
            perror("ERROR creating socket");
            return NULL;
        }

        struct sockaddr_in servaddr;
        memset(&servaddr, 0, sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        servaddr.sin_addr.s_addr = inet_addr(ip);
        servaddr.sin_port = htons(12345);
        socklen_t serv_length = sizeof(servaddr);
        
        
        
        
        if (sendto(sock, message, strlen(message), 0, (struct sockaddr*)&servaddr, serv_length) < 0) {
            perror("Failed sending broadcast message");
        } else {
            int fd = open("/Users/duy/Desktop/demo.log", O_RDWR | O_APPEND);
            write(fd, "Successfully sent", strlen("Successfully sent"));
            write(fd, "\n", 1);
            close(fd);
        }
        close(sock);
    }
    free(ip);
    return NULL;
}

struct arg {
    char*** hostIPs;
    char*** roomNames;
};

void *receiveResponseThread(void *arg) {
    char ***hostIPs = ((struct arg*)arg)->hostIPs;
    char ***roomNames = ((struct arg*)arg)->roomNames;
    
    int responseSocketFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (responseSocketFd < 0) {
        perror("ERROR creating socket for handling response");
        return NULL;
    }
    
    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(54321);
    socklen_t serv_length = sizeof(servaddr);
    
    struct timeval tv;
    tv.tv_sec = 5;
    tv.tv_usec = 0;
    
    if (setsockopt(responseSocketFd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv)) < 0) {
        perror("ERROR setting socket option");
    }
    
    if (bind(responseSocketFd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("ERROR binding socket");
    }
    
    char buffer[64];
    
    for (int i=0; i<50; i++) {
        if (recvfrom(responseSocketFd, buffer, 63, 0, (struct sockaddr*)&servaddr, &serv_length) < 0) {
            close(responseSocketFd);
            return NULL;;
        } else {
            int fd = open("/Users/duy/Desktop/demo.log", O_RDWR | O_APPEND);
            write(fd, "Successfully received response", strlen("Successfully received response"));
            write(fd, "\n", 1);
            close(fd);
            if (strncmp(buffer, "!Active", 7) == 0) {
                // Receive IP adress
                
                char **result = NULL;
                // Receive room name
                split(buffer, " ", &result);
                

                
                for (int i=0; i<MAX_ROOMS; ++i) {
                    if ((*hostIPs)[i] == NULL) {
                        (*hostIPs)[i] = malloc(16);
                        inet_ntop(AF_INET, &(servaddr.sin_addr), (*hostIPs)[i], 15);
                        (*hostIPs)[i][15] = '\0';
                    }
                    
                    if ((*roomNames)[i] == NULL) {
                        (*roomNames)[i] = malloc(32);
                        strncpy((*roomNames)[i], result[1], strlen(result[1]));
                        
                        int fd = open("/Users/duy/Desktop/demo.log", O_RDWR | O_APPEND);
                        write(fd, (*roomNames)[i], strlen((*roomNames)[i]));
                        write(fd, "\n", 1);
                        close(fd);
                        
                        break;
                    }
                }
            }
        }
    }
    return NULL;
}

// The function @discoverRoom is used to discover if there are any active room in current LAN
// @parameters: {
//  @hostIPs: used to write the ip address of discovered room's host
//  @roomNames: used to write the room name of discovered room
// }
// @return: 0 if successfully discorver the rooms or -1 if not
int discoverRoom(char*** hostIPs, char*** roomNames) {
    // Step 1: send to all IP in LAN the following package:
    //      Package's content: ?DiscoverRoom
    // Step 2: wait for the response
    // Step 3: write the response to @hostIPs and @roomNames

    

    if (hostIPs == NULL || roomNames == NULL) return -1;
    if (*hostIPs == NULL) {
        *hostIPs = malloc(MAX_ROOMS*sizeof(char*));
        for (int i=0; i<MAX_ROOMS; ++i) {
            (*hostIPs)[i] = NULL;
        }
    }
    if (*roomNames == NULL) {
        *roomNames = malloc(MAX_ROOMS*sizeof(char*));
        for (int i=0; i<MAX_ROOMS; ++i) {
            (*roomNames)[i] = NULL;
        }
    }

    // Get the IP address and netmask of the current interface
    struct ifaddrs *ifaddr, *ifa;
    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return 1;
    }

    char* base_ip = NULL;
    struct sockaddr_in* netmask = NULL;
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL) continue;

        if (ifa->ifa_addr->sa_family == AF_INET) {
            // This is an IPv4 address
            struct sockaddr_in *addr = (struct sockaddr_in *)ifa->ifa_addr;

            // If the interface is the loopback interface, ignore it
            if (strcmp(ifa->ifa_name, "lo0") == 0) continue;

            // Get the netmask for this interface
            struct sockaddr_in *mask = (struct sockaddr_in *)ifa->ifa_netmask;

            // Convert the netmask to binary
            netmask = (struct sockaddr_in *)malloc(sizeof(struct sockaddr_in));
            memset(netmask, 0, sizeof(struct sockaddr_in));
            netmask->sin_family = AF_INET;
            netmask->sin_addr.s_addr = mask->sin_addr.s_addr;

            // Determine the base IP for the LAN
            base_ip = (char*)malloc(INET_ADDRSTRLEN * sizeof(char));
            memset(base_ip, 0, INET_ADDRSTRLEN * sizeof(char));
            strncpy(base_ip, inet_ntoa(addr->sin_addr), INET_ADDRSTRLEN);
            char* pch = strrchr(base_ip, '.');
            if (pch != NULL) *pch = '\0';
            strcat(base_ip, ".");

            break;
        }
    }
    freeifaddrs(ifaddr);
    
    
    pthread_t sendDiscoveringTid, receiveResponseTid;
    
    pthread_create(&sendDiscoveringTid, NULL, sendDiscoveringMessageThread, base_ip);
    
    struct arg response = {hostIPs, roomNames};
    pthread_create(&receiveResponseTid, NULL, receiveResponseThread, &response);
    
    pthread_join(receiveResponseTid, NULL);
    pthread_join(sendDiscoveringTid, NULL);
    


    free(base_ip);
    free(netmask);

    return 0;
}

int main(int argc, char **argv) {
    char **hostIPs = NULL;
    char **roomNames = NULL;
    
    discoverRoom(&hostIPs, &roomNames);
    for (int i=0; hostIPs[i] != NULL; i++) {
        char *buffer = malloc(64);
        sprintf(buffer, "%s: %s\n", roomNames[i], hostIPs[i]);
        fputs(buffer, stdout);
        free(buffer);
    }
}

// ++++++++++++++++++++++++++++++++++++++++++++ Discover Room ++++++++++++++++++++++++++++++++++++++++++++ //
