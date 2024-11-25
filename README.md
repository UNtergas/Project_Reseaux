## Project Reseaux

An continuation with the project of the first semester, Ceasar 3.
This project is about the implementation of a network with peer to peer communication.

#### Architecture
The game will be run on python as normally, and the C layer will be the one that will handle the network communication.
The communication between the python and C layer will be done through IPC (Inter Process Communication). The game state 
will be transmitted through the network, and the game will be synchronized between the players.

The peer to peer communication will be done through the TCP protocol. With the idea that each player will create a 
room and the other players will join that room.

