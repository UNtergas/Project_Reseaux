import pygame as py
from multiplayer import multi
from Scene import *
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scenes.Scene_ids import *


def SceneMultiCreate(self):
    self.playerName = None
    self.box = {}
    createRoom = Button(py.Rect(200, 350, 150, 50), "Create Room",
                        font_button, None, event_types["CreateRoom"])
    joinRoom = Button(py.Rect(450, 350, 150, 50), "Join Room",
                      font_button, None, event_types["JoinRoom"])
    back = Button(py.Rect(50, 550, 100, 50), "Back",
                  font_button, switchScene, SCENE_MENU_ID)
    self.buttons = [createRoom, joinRoom, back]


def RoomCreate(self, playerName: str):
    success, room_id = multi.create_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiJoin(self):
    # self.playerName = BOXES["playerName"].getText()
    self.box = {}
    joinRoom = Button(py.Rect(200, 350, 150, 50), "Join Room",
                      font_button, None, event_types["JoinRoom"])
    back = Button(py.Rect(50, 550, 100, 50), "Back",
                  font_button, switchScene, SCENE_MENU_ID)
    self.buttons = [joinRoom, back]


def RoomJoin(self, playerName: str):
    success, room_id = multi.join_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiRun(self):
    pass


def SceneEventHandler(self, event):
    if event.type == event_types["CreateRoom"]:
        RoomCreate(self, self.playerName)
    elif event.type == event_types["JoinRoom"]:
        RoomJoin(self, self.playerName)


SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi',
              createFunc=SceneMultiCreate, runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)


"""
#But de ces fichiers : Creer interface Multi-jeu
#Voir aussi les fichiers : Scene_multicreate.py, Scene_multijoin.py
#Voir les autres fichiers Scene pour exemple

import pygame as py
from const import font1,font_button
from Button import *
from Inputbox import InputBox
from Scene_ids import *
from Scene import *

def SceneMultiCreate(self):
    pass
    text = font1.render("Your name: ") #input
    box['player'] = InputBox()
    create = Button() #event_type['CreateRoom']
    join = Button() #event_type['JoinRoom']
    exit = Button() #switchScene(SCENE_MENU_ID)

def SceneMultiRun(self):
    pass
    #dessiner la carte ici

def SceneEventHandler(self,event):
    pass
    if event.type == event_types["CreateRoom"]:
        self.game.switchScene(SCENE_MULTI_CREATE_ID)
    if event.type == event.types["JoinRoom"]:
        self.game.switchScene(SCENE_MULTI_JOIN_ID)

SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)