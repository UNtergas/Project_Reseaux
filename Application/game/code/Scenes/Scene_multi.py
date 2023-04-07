import pygame as py
from multiplayer import multi
from Scene import *
from const import *
from Button import *
from Inputbox import InputBox
from Scenes.Scene_ids import *
from Save import *
from Utils import GenerateGridLayout


def SceneMultiCreate(self):
    self.images["fond"] = pygame.image.load(
        "assets/0_fired_00001.png").convert()

    layout = GenerateGridLayout(
        self.game.screen_width/2, self.game.screen_height/2, 1, 4, 0, 50, 300, 100)

    self.buttons["Create"] = Button_text(
        *next(layout), 300, 100, lambda: self.game.switchScene(SCENE_MULTI_CREATE_ID), "Create room", font1)

    self.buttons["Join"] = Button_text(
        *next(layout), 300, 100, lambda: self.game.switchScene(SCENE_MULTI_JOIN_ID), "Join room", font1)

    self.buttons["button_menu"] = Button_text(
        *next(layout), 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Exit", font1)


def SceneMultiRun(self):

    pygame.time.Clock().tick(60)
    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen)

    pygame.display.flip()


SCENE = Scene(SCENE_MULTI_ID, 'Scene_Multi', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun)


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
