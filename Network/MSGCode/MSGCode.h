//
//  MSGCode.h
//  internet_project
//
//  Created by Pham Duy on 28/03/2023.
//

#ifndef MSGCode_h
#define MSGCode_h

#include <stdio.h>
#include "../Session/Session.h"

int roomToStr(Room room, char *buffer); // This function is used to encode room in4 to a string
int strToRoom(char *buffer, Room *room); // This function is used to decode string to room in4

#endif /* MSGCode_h */

