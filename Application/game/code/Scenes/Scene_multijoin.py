import pygame as py
from multiplayer import multi
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scene_ids import *
from Scene import *


def SceneRoomCreate(self):
    pass
    text = font1.render("Room name: ")  # input
    box['room'] = InputBox()
    create = Button()  # event_type['CreateRoom']
    exit = Button()  # switchScene(SCENE_MENU_ID)


def JoinRooms(roomName: str, playerName: str):
    pass
    join(roomName, playerName)
    # appeler fonction join


def ShowRoom(self, playerName: str):
    pass
    rooms = []
    rooms = getAvailableRoom()  # afficher les noms des rooms


def SceneMultiRun(self):
    pass
    # dessiner la  carte ici


def SceneEventHandler(self, event):
    pass
    # if event.type == event_types["JoinRoom"]:
    #     JoinRooms(roomName,playerName)


SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)
