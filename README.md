# Project_Reseaux

The network project is dedicated for creating a multi-player game using LAN. The very final objectif of this project is to create an efficient, robust and easy-to-play game. We use the older Caesar III project written by Python as the main game. After that we use C as the programming language to build our network. And for the communicating between the game (written by Python) and the network module (written by C), we use message queue as the inter process communication technique.

The network project is dedicated for creating a multi-player game using LAN. The very final objectif of this project is to create an efficient, robust and easy-to-play game. We use the older Caesar III project written by Python as the main game. After that we use C as the programming language to build our network. And for the communicating between the game (written by Python) and the network module (written by C), we use message queue as the inter process communication technique.

<h2>Software architecture</h2>

```
       --------                         --------
       | Game |                         | Game |
       --------                         --------
          |                                 ^
          v                                 |
     -----------                       -----------
     | Encoder |                       | Decoder |
     -----------                       -----------
          |                                 ^
          v                                 |
-----------------------           -----------------------
|         NI          |           |         NI          |
| (Network Interface) |           | (Network Interface) |
-----------------------           -----------------------
          |                                 ^
          V                                 |
          -----------------------------------
```

The good architecture for network system is often (if not always) layers architecture. In this project, we have decided to create a 3-layers architecture as above. So if a player need to send the package containing the game's information, the package will be encoded by `encoder` and then is delivred to `Network Interface` to be transported in the network. After that, the rest players of game will receive the package via their own `Network Interface` and will be decoded by `Decoder` before being used to update their own game state. So:

- layer 0 (NI) is used to communicate between client at the level of network via TCP protocol (layer 4 in OSI model).
- layer 1 (encoder and decoder): is used to make sure that the data will be formated in the right way to transfer among clients (layer 6 in OSI model)
- layer 2 (Game): is the terminal application that clients use to interact with other (layer 7 in OSI model).


## compile && run
```
chmod +400 lan/compile.sh
./lan/compile.sh
```

## TODO List
```


```

# Task for each person
```
Yacine: Multi-player Scence (go to Application/code/Scenes/Scene_multi.py)✅
Duke: IPC (go to Presentation/IO.py)✅
Tuan: IPC (go to Presentation/IPC.py and IO.py)✅
Khang: Session (go to Session/Room.c)🔜
Duy: Network 🔜
Phong: Multi-player logic (go to Application/multi)✅
# Rapport
   - [ ] Intro : Khang + Yacine 
   - [ ] Method : Duy + Phong 
   - [ ] Architecture Réseaux : Duke 
   - [ ] Architecture Système : Tuan 
   - [ ] Conclusion : Khang + Yacine 
```

