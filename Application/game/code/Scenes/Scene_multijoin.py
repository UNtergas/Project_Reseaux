import pygame as py
from multiplayer import multi
from Scene import *
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scenes.Scene_ids import *


def SceneMultiCreate(self):
    # Text and input for room name
    text = font1.render("Room name: ", True, (0, 0, 0))
    self.box = {}
    self.box['room'] = InputBox(300, 350, 400, 50, text=text)

    # Buttons for creating room and going back to menu
    create_text = font_button.render("Create Room", True, (0, 0, 0))
    self.create_button = Button(
        300, 425, 150, 50, create_text, event_type=event_types['CreateRoom'])

    back_text = font_button.render("Back", True, (0, 0, 0))
    self.back_button = Button(
        550, 425, 150, 50, back_text, switch_to_scene=SCENE_MENU_ID)

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
    # Handling events
    if event.type == event_types["CreateRoom"]:
        RoomCreate(self, self.playerName)


SCENE = Scene(SCENE_MULTI_JOIN_ID, 'Scene_multicreate', createFunc=SceneMultiCreate,
                           runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)


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
