import pygame as py
from multiplayer import multi
from Scene import *
from const import *
from Button import *
from Inputbox import InputBox
from Scenes.Scene_ids import *
from Save import *


def SceneMultiCreate(self):
    self.images["fond"] = pygame.image.load(
        "assets/01b_00001.png").convert()
    self.playerName = None
    self.box = {}
    # Utilisation de la variable font1 pour le rendu du texte
    text = font1.render("Room name: ", True, (255, 255, 255))  # input
    self.box['room'] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45, lambda: py.event.post(py.event.Event(
            event_types["Create"], {"name": 1})), font2)

    self.buttons['create'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                         2+50, 300, 100, lambda: self.game.switchScene(SCENE_MULTI_CREATE_ID), "Create room")
    # Modification du nom d'un bouton pour qu'ils soient uniques
    self.buttons['join_room'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                            2+50, 300, 100, lambda: self.game.switchScene(SCENE_MULTI_JOIN_ID), "Join room")
    self.buttons['exit'] = Button_text(self.game.screen_width/2-150, self.game.screen_height /
                                       2+50, 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Back to Menu")


def RoomCreate(self, playerName: str):
    success, room_id = multi.create_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiJoin(self):
    self.box = {}
    joinRoom = Button(py.Rect(200, 350, 150, 50), "Join Room",
                      font_button, None, event_types["JoinRoom"])

    back = font_button.render("Back to menu", True, (0, 0, 0))
    self.back_button = Button_text(
        550, 425, 150, 50, lambda: self.game.switchScene(SCENE_MENU_ID), "back to menu", font_button)

    # Utilisation d'un dictionnaire pour stocker les boutons
    self.buttons = {"join_room": joinRoom, "back": back}


def RoomJoin(self, playerName: str):
    success, room_id = multi.join_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiRun(self):
    pygame.time.Clock().tick(60)

    print('Multi scene running')

    self.game.screen.fill((255, 255, 255))

    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))

    pygame.draw.rect(self.game.screen, (180, 180, 180),
                     (self.game.screen_width/2-300, self.game.screen_height/2-100, 600, 175))

    print("Drawing buttons")

    for key in self.box.keys():
        self.box[key].show(self.game.screen)

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen, False)

    print("Drawing text")

    text = font1.render("Enter the name of your room", 1, (0, 0, 0))
    self.game.screen.blit(text, (self.game.screen_width /
                          2-text.get_width()/2, self.game.screen_height/2-100))


def SceneEventHandler(self, event):
    # Suppression d'un paramètre inutilisé
    pass


SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi',
              createFunc=SceneMultiCreate, runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)

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
    self.images["fond"] = pygame.image.load(
        "assets/01b_00001.png").convert()
    self.playerName = None
    self.box = {}
    # Utilisation de la variable font1 pour le rendu du texte
    text = font1.render("Room name: ", True, (255, 255, 255))  # input
    self.box['room'] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45, lambda: py.event.post(py.event.Event(
            event_types["Create"], {"name": 1})), font2)

    self.buttons['create'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                         2+50, 300, 100, lambda: self.game.switchScene(SCENE_MULTI_CREATE_ID), "Create room")
    # Modification du nom d'un bouton pour qu'ils soient uniques
    self.buttons['join_room'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                            2+50, 300, 100, lambda: self.game.switchScene(SCENE_MULTI_JOIN_ID), "Join room")
    self.buttons['exit'] = Button_text(self.game.screen_width/2-150, self.game.screen_height /
                                       2+50, 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Back to Menu")


def RoomCreate(self, playerName: str):
    success, room_id = multi.create_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiJoin(self):
    self.box = {}
    joinRoom = Button(py.Rect(200, 350, 150, 50), "Join Room",
                      font_button, None, event_types["JoinRoom"])

    back = font_button.render("Back to menu", True, (0, 0, 0))
    self.back_button = Button_text(
        550, 425, 150, 50, lambda: self.game.switchScene(SCENE_MENU_ID), "back to menu", font_button)

    # Utilisation d'un dictionnaire pour stocker les boutons
    self.buttons = {"join_room": joinRoom, "back": back}


def RoomJoin(self, playerName: str):
    success, room_id = multi.join_room(self.box['room'].text, playerName)
    if success:
        self.game.switchScene(SCENE_GAME_ID, room_id)


def SceneMultiRun(self):
    pygame.time.Clock().tick(60)

    print('Multi scene running')

    self.game.screen.fill((255, 255, 255))

    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))

    pygame.draw.rect(self.game.screen, (180, 180, 180),
                     (self.game.screen_width/2-300, self.game.screen_height/2-100, 600, 175))

    print("Drawing buttons")

    for key in self.box.keys():
        self.box[key].show(self.game.screen)

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen, False)

    print("Drawing text")

    text = font1.render("Enter the name of your room", 1, (0, 0, 0))
    self.game.screen.blit(text, (self.game.screen_width /
                          2-text.get_width()/2, self.game.screen_height/2-100))


def SceneEventHandler(self, event):
    # Suppression d'un paramètre inutilisé
    pass


SCENE = Scene(SCENE_MULTI_ID, 'Scene_multi',
              createFunc=SceneMultiCreate, runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)
"""

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
"""
