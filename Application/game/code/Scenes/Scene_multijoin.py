import pygame as py
from multiplayer import multi
from Scene import *
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scene_ids import *


def SceneRoomCreate(self):
    pass
    # text = font1.render("Room name: ")  # input
    # box['room'] = InputBox()
    # create = Button()  # event_type['CreateRoom']
    # exit = Button()  # switchScene(SCENE_MENU_ID)


def RoomCreate(self, playerName: str):
    pass
    # if (createroom(self.box['room'], playerName)) self.game.switchScene(SCENE_GAME_ID)
    # # rappeller function createRoom(roomName, playerName)
    # # avec success,  switch to game


def SceneMultiRun(self):
    pass
    # draw Scene ici


def SceneEventHandler(self, event):
    pass
    # if event.type == event_types["CreateRoom"]:
    #     RoomCreate(self.playerName)


SCENE = Scene(SCENE_MULTI_JOIN_ID, 'Scene_multijoin', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)
