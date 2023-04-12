from Scene import *
import pygame
from Button import *
from Inputbox import InputBox
from Save import *
from const import *
from .Scene_ids import *
from multiplayer.multi import *
import socket


def SceneMultiCreate(self):
    self.images["fond"] = pygame.image.load(
        "assets/01b_00001.png").convert()

    self.box["inputbox"] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-90, 600, 45, lambda: pygame.event.post(pygame.event.Event(
            event_types["LaunchGame"], {"name": 1})), font2)

    self.box["namebox"] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2, 600, 45, lambda: None, font2)

    self.buttons['button_menu'] = Button_text(self.game.screen_width/2-150, self.game.screen_height /
                                              2+50, 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Back to Menu")
    self.buttons['create_button'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                                2+50, 300, 100, lambda: pygame.event.post(pygame.event.Event(
                                                    event_types["LaunchGame"], {"name": 1})), "Create your room")


def SceneMultiCreateRun(self):

    pygame.time.Clock().tick(60)

    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))

    pygame.draw.rect(self.game.screen, (180, 180, 180),
                     (self.game.screen_width/2-300, self.game.screen_height/2-100, 600, 175))

    for key in self.box.keys():
        self.box[key].show(self.game.screen)

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen, False)

    text = font1.render("Enter the name of your room", 1, (0, 0, 0))
    self.game.screen.blit(text, (self.game.screen_width /
                          2-text.get_width()/2, self.game.screen_height/2-150))

    text = font1.render("Enter your name", 1, (0, 0, 0))
    self.game.screen.blit(text, (self.game.screen_width /
                          2-text.get_width()/2, self.game.screen_height/2-60))

    pygame.display.flip()


def SceneEventHandler(self, event):
    if event.type == event_types["LaunchGame"]:
        socket = createRoom(self.box['inputbox'].text, self.box["namebox"].text)
        self.game.save = Save(self.box["inputbox"].text, socket)
        self.game.switchScene(SCENE_GAME_ID)
        self.box['inputbox'].text = ""


# Create the scene object
SCENE = Scene(SCENE_MULTI_CREATE_ID, 'Scene_multicreate', createFunc=SceneMultiCreate,
              runFunc=SceneMultiCreateRun, handleEventsFunc=SceneEventHandler)


"""
import pygame as py
from multiplayer import multi
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


def SceneMultiCreateRun(self):
    pass
    # dessiner la  carte ici


def SceneEventHandler(self, event):
    pass
    # if event.type == event_types["JoinRoom"]:
    #     JoinRooms(roomName,playerName)


SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi', createFunc=SceneMultiCreate,
              runFunc=SceneMultiCreateRun, handleEventsFunc=SceneEventHandler)
"""
