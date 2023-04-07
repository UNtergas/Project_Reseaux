//
//  Error.c
//  internet_project
//
//  Created by Pham Duy on 27/03/2023.
//

#include "Support.h"

#include <stdio.h>
#include <netdb.h>
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

void stop(char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

int split(char *str, char *delim, char ***result) {
    char *tmp = str;
    
    int num_token = 1; // initialize to 1 for case where input string is empty
    while (*tmp != '\0') {
        if (strncmp(tmp, delim, strlen(delim)) == 0) {
            num_token++;
        }
        tmp++;
    }
    
    *result = malloc(num_token * sizeof(char*));
    
    int count = 0; // counter of the current length of a token
    int current_token = 0;
    tmp = str;
    while (*tmp != '\0') {
        if (strncmp(tmp, delim, strlen(delim)) == 0) {
            (*result)[current_token] = malloc(count + 1);
            strncpy((*result)[current_token], tmp - count, count);
            (*result)[current_token][count] = '\0';
            count = 0;
            current_token += 1;
        } else {
            count += 1;
        }
        tmp++;
    }
    
    // handle case where input string ends with delimiter
    if (count > 0) {
        (*result)[current_token] = malloc(count + 1);
        strncpy((*result)[current_token], tmp - count, count);
        (*result)[current_token][count] = '\0';
    }
    
    return num_token;
}

void getMyIP(char *myIP) {
    // Get the IP address and netmask of the current interface
    struct ifaddrs *ifaddr, *ifa;
    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return;
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


            if (inet_ntop(AF_INET, &addr->sin_addr, myIP, NI_MAXHOST) == NULL) {
                perror("inet_ntop");
                continue;
            } 
            if (strcmp(myIP, "127.0.0.1\0") == 0)
                continue;
            else return;
        }
    }

    freeifaddrs(ifaddr);
}

