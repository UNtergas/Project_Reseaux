#!/bin/bash

# install requirements
pip install requirements.txt

# compile file .c
gcc -c **/*.c; 
gcc -c Network/main.c;

# link object files
gcc *.o -o app

# clean directory
rm *.o

# run the game and network module
./app # have not yet completed

