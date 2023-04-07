import pygame
from Scene import Scene
from Button import Button_text
from Inputbox import InputBox
from const import *
from Scenes.Scene_ids import *
from multiplayer import multi


def SceneMultiCreate(self):
    self.box = {}
    text = font1.render("Room name: ", True, (0, 0, 0))
    self.box['room'] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45, lambda: pygame.event.post(pygame.event.Event(
            event_types["Create"], {"name": 1})), font2)

    self.buttons = {}
    self.back_button = Button_text(
        550, 425, 150, 50, lambda: self.game.switchScene(SCENE_MENU_ID), "Back")
    self.buttons['join'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                       2+50, 300, 100, lambda: pygame.event.post(pygame.event.Event(
                                           event_types["JoinRoom"], {"name": 1})), "Join room")


"""
    self.addObject(self.box['room'])
    self.addObject(self.back_button)
    self.addObject(self.buttons['join'])
"""


def SceneMultiRun(self):
    self.game.screen.fill((255, 255, 255))
    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen, False)
    pygame.display.flip()


def SceneEventHandler(self, event):
    pass


def RoomCreate(self, playerName: str):
    success = multi.createRoom(self.box['room'].getText(), playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID)


SCENE = Scene(SCENE_MULTI_JOIN_ID, 'Scene_multicreate', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)


"""
import pygame as py
from multiplayer import multi
from Scene import *
from const import *
from Button import *
from Inputbox import InputBox
from Scenes.Scene_ids import *
from Save import *


def SceneMultiCreate(self):
    # Text and input for room name
    text = font1.render("Room name: ", True, (0, 0, 0))
    self.box = {}
    self.box['room'] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45, lambda: py.event.post(py.event.Event(
            event_types["Create"], {"name": 1})), font2)

    # Buttons for joinning room and going back to menu
    back_text = font_button.render("Back", True, (0, 0, 0))
    self.back_button = Button_text(
        550, 425, 150, 50, lambda: self.game.switchScene(SCENE_MENU_ID), back_text)

    self.buttons['join'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                       2+50, 300, 100, lambda: pygame.event.post(pygame.event.Event(
                                           event_types["JoinRoom"], {"name": 1})), "Join room")
    # Adding objects to the Scene object
    self.addObject(self.box['room'])
    self.addObject(self.create_button)
    self.addObject(self.back_button)


def RoomCreate(self, playerName: str):
    success = multi.createRoom(self.box['room'].getText(), playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID)


def SceneMultiRun(self):
    # Drawing the Scene
    self.screen.fill((255, 255, 255))
    for obj in self.objects:
        obj.draw(self.screen)
    py.display.flip()


def SceneEventHandler(self, event):
    pass


SCENE = Scene(SCENE_MULTI_JOIN_ID, 'Scene_multicreate', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)
"""

"""import pygame as py
from multiplayer import multi
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scene_ids import *
from Scene import *


def SceneRoomCreate(self):
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
"""
