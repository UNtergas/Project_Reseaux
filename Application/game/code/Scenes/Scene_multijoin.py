from Scene import *
import pygame
from Button import *
from Inputbox import InputBox
from Save import *
from const import *
from .Scene_ids import *
from multiplayer.multi import *


def SceneMultiJoin(self):
    self.images["fond"] = pygame.image.load(
        "assets/01b_00001.png").convert()

    self.box["inputbox"] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45, lambda: pygame.event.post(pygame.event.Event(
            event_types["LaunchGame"], {"name": 1})), font2)

    self.buttons['button_menu'] = Button_text(self.game.screen_width/2-150, self.game.screen_height /
                                              2+50, 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Back to Menu")
    self.buttons['join_button'] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                              2+50, 300, 100, lambda: pygame.event.post(pygame.event.Event(
                                                  event_types["LaunchGame"], {"name": 1})), "Join your room")


def SceneMultiJoinRun(self):

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
                          2-text.get_width()/2, self.game.screen_height/2-100))

    pygame.display.flip()


def SceneEventHandler(self, event):
    if event.type == event_types["LaunchGame"]:
        rooms = getAvailableRoom()
        for room in rooms:
            if room["roomName"] == self.box["inputbox"].text:
                join(room["hostIP"],'John')
            break
        self.game.save = Save(self.box["inputbox"].text)
        self.game.switchScene(SCENE_GAME_ID)
        self.box['inputbox'].text = ""


# Create the scene object
SCENE = Scene(SCENE_MULTI_JOIN_ID, 'Scene_multicreate', createFunc=SceneMultiJoin,
              runFunc=SceneMultiJoinRun, handleEventsFunc=SceneEventHandler)


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
