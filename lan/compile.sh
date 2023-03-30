#!/bin/bash

# compile file .c
gcc -c **/*.c; 
gcc -c main.c;

# link object files
gcc *.o -o app

# clean directory
rm *.o
