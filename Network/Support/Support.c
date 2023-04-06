//
//  Error.c
//  internet_project
//
//  Created by Pham Duy on 27/03/2023.
//

#include "Support.h"
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>

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

