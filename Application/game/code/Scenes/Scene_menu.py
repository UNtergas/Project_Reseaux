from Scene import *
import pygame
from Button import *
from const import *
from .Scene_ids import SCENE_MENU_ID, SCENE_GAME_ID, SCENE_NEWGAME_ID, SCENE_LOADGAME_ID
from Utils import GenerateGridLayout


def SceneMenuCreate(self):
    self.images["fond"] = pygame.image.load(
        "assets/0_fired_00001.png").convert()

    # GENERATE GRID LAYOUT 1 column 4 rows centered on self.game.screen_width/2, self.game.screen_height/2
    #         200 px
    #         -------
    # 100 px |       |
    #         -------
    # 50px
    #         -------
    # 100 px |       |
    #         -------
    # 50 px
    #         -------
    # 100 px |       |
    #         -------
    # 50px
    #         -------
    # 100 px |       |
    #         -------

    layout = GenerateGridLayout(
        self.game.screen_width/2, self.game.screen_height/2, 1, 4, 0, 50, 300, 100)

    self.buttons["button_start"] = Button_text(
        *next(layout), 300, 100, lambda: self.game.switchScene(SCENE_NEWGAME_ID), "Start Game", font1)
    self.buttons["button_load"] = Button_text(
        *next(layout), 300, 100, lambda: self.game.switchScene(SCENE_LOADGAME_ID), "Load a Game", font1)
    self.buttons["button_options"] = Button_text(
        *next(layout), 300, 100, lambda: print("ok"), "Options", font1)
    self.buttons["button_exit"] = Button_text(
        *next(layout), 300, 100, self.game.end, "Exit Game", font1)


def SceneMenuRun(self):

    pygame.time.Clock().tick(60)
    self.game.screen.blit(pygame.transform.scale(
        self.images["fond"], (self.game.screen_width, self.game.screen_height)), (0, 0))

    for key in self.buttons.keys():
        self.buttons[key].show(self.game.screen)

    pygame.display.flip()


SCENE = Scene(SCENE_MENU_ID, 'Scene_Menu', createFunc=SceneMenuCreate,
              runFunc=SceneMenuRun)
