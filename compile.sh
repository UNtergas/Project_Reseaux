gcc -c **/**/*.c; gcc -c Network/main.c; rm getAvailableRoom.o ;gcc *.o -o app; rm *.o
gcc getAvailableRoom.c Network/Support/Support.c -o getAvailableRoom
mv app getAvailableRoom executable
