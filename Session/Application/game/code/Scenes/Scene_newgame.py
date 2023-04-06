from Scene import *
import pygame
from Button import *
from Inputbox import InputBox
from Save import *
from const import *
from .Scene_ids import *


def SceneNewGameCreate(self):
    self.images["fond"] = pygame.image.load(
        "assets/01b_00001.png").convert()

    self.box["inputbox"] = InputBox(
        self.game.screen_width/2, self.game.screen_height/2-30, 600, 45,  lambda : pygame.event.post(pygame.event.Event(
            event_types["LaunchGame"], {"name": 1})), font2)

    self.buttons["btn1"] = Button_text(self.game.screen_width/2-150, self.game.screen_height /
                                       2+50, 300, 100, lambda: self.game.switchScene(SCENE_MENU_ID), "Back to Menu")
    self.buttons["btn2"] = Button_text(self.game.screen_width/2+150, self.game.screen_height /
                                       2+50, 300, 100, lambda: pygame.event.post(pygame.event.Event(
                                           event_types["LaunchGame"], {"name": 1})), "Go to Game")


def SceneNewGameRun(self):

    pygame.time.Clock().tick(60)
    
    
    
    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))
    
    pygame.draw.rect(self.game.screen, (180,180,180), (self.game.screen_width/2-300, self.game.screen_height/2-100, 600, 175))

    for key in self.box.keys():
        self.box[key].show(self.game.screen)

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen, False)
    
    text = font1.render("Enter the name of your save",1, (0,0,0))
    self.game.screen.blit(text, (self.game.screen_width/2-text.get_width()/2, self.game.screen_height/2-100))
        
        

    pygame.display.flip()


def SceneNewGamehandleEventsFunc(self, event):
    if event.type == event_types["LaunchGame"]:
        print(event)
        self.game.save = Save(self.box["inputbox"].text)
        self.game.switchScene(SCENE_GAME_ID)
        self.box['inputbox'].text = ""


SCENE = Scene(SCENE_NEWGAME_ID, 'Scene_newgame', createFunc=SceneNewGameCreate,
              runFunc=SceneNewGameRun, handleEventsFunc=SceneNewGamehandleEventsFunc)
