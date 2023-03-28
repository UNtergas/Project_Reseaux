//
//  Error.c
//  internet_project
//
//  Created by Pham Duy on 27/03/2023.
//

#include "Error.h"
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>

void stop(char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}
