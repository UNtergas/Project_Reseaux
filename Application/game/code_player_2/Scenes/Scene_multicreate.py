import pygame as py
from multiplayer import multi
from Scene import *
from const import font1, font_button
from Button import *
from Inputbox import InputBox
from Scene_ids import *

# Define constants for button sizes
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2

# Define a constant for the input box size
INPUT_WIDTH = 300
INPUT_HEIGHT = 50
INPUT_SPACING = 10
INPUT_X = (SCREEN_WIDTH - INPUT_WIDTH) // 2
INPUT_Y = 150

# Define a dictionary to store input boxes
BOXES = {}


def SceneMultiCreate(self):
    # Create an input box for the room name
    BOXES["room"] = InputBox(
        INPUT_X, INPUT_Y, INPUT_WIDTH, INPUT_HEIGHT, "Room Name", font1)

    # Create a button to create the room
    create_button = Button(BUTTON_X, INPUT_Y + INPUT_HEIGHT + INPUT_SPACING,
                           BUTTON_WIDTH, BUTTON_HEIGHT, "Create Room", font_button, self.create_room)

    # Create a button to go back to the main menu
    back_button = Button(BUTTON_X, BUTTON_Y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH,
                         BUTTON_HEIGHT, "Back", font_button, self.switch_scene, SCENE_MENU_ID)

    # Add the buttons to the scene
    self.addButton(create_button)
    self.addButton(back_button)


def create_room(self):
    # Get the room name from the input box
    room_name = BOXES["room"].getText()

    # Check that the room name is not empty
    if room_name != "":
        # Create the room
        if multi.create_room(room_name, self.playerName):
            # If successful, switch to the game scene
            self.game.switchScene(SCENE_GAME_ID)


def SceneMultiRun(self):
    # Draw the input box
    BOXES["room"].draw(self.game.screen)

    # Draw the buttons
    self.drawButtons()


def SceneEventHandler(self, event):
    # Handle events for the input box
    BOXES["room"].handle_event(event)


# Create the scene object
SCENE = Scene(SCENE_MULTI_CREATE_ID, 'Scene_multicreate', createFunc=SceneMultiCreate,
              runFunc=SceneMultiRun, handleEventsFunc=SceneEventHandler)


"""
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
"""
