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