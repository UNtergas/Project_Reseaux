import pygame as pg
from .Button import *
from .Game_event import *


class InfoShow:
    def __init__(self, x, y, text, font_size, color):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color
        self.box = pg.image.load(
            "ingamehud/paneling_00015.png").convert_alpha()
        self.rect = pg.Rect(x, y, self.box.get_width(), self.box.get_height())

    def draw(self, screen):
        screen.blit(self.box, (self.x, self.y))
        font = pg.font.SysFont(None, self.font_size)
        text_surface = font.render(self.text, True, self.color)
        text_rect = pygame.Rect(
            self.x+10, self.y+5, text_surface.get_width(), text_surface.get_height())
        screen.blit(text_surface, text_rect)


class Hudupper:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.image = pg.image.load(
            "ingamehud/paneling_00235.png").convert_alpha()
        self.rect = pg.Rect(x, y, width, self.image.get_height())

    def draw(self, screen):
        screen.blit(pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height)), self.rect)


class Hudbigleft:
    def __init__(self, width, height):

        #button in interaction
        self.interaction = None
        self.width = width
        self.height = height

        self.paneling_017 = pg.image.load(
            "ingamehud/paneling_00017.png").convert_alpha()

        self.rect = pg.Rect((self.width - 162, 25),
                            (self.paneling_017.get_width(), self.height-25))

        self.map_panels_00003 = pg.image.load(
            "ingamehud/map_panels_00003.png").convert_alpha()
        self.panelwindow_013 = pg.image.load(
            "ingamehud/panelwindows_00013.png").convert_alpha()
        #hud in out
        self.button_098 = Button_img(
            self.width-20, 20+21, "ingamehud/paneling_00098.png")
        # gap 77/ 2 long af button
        self.button_080 = Button_img(
            self.width-120, 170+21, "ingamehud/paneling_00080.png")
        self.button_082 = Button_img(
            self.width-43, 170+21,  "ingamehud/paneling_00082.png")
        # gap 39 /small button
        self.button_085 = Button_img(
            self.width-139, 199+21,  "ingamehud/paneling_00085.png")
        self.button_088 = Button_img(
            self.width-100, 199+21,  "ingamehud/paneling_00088.png")
        self.button_091 = Button_img(
            self.width-62, 199+21,  "ingamehud/paneling_00091.png")
        self.button_094 = Button_img(
            self.width-23, 199+21,  "ingamehud/paneling_00094.png")
        # gap width 50 gap height 36 /big button
        self.button_123 = Button_img(
            self.width-130, 294+21,  "ingamehud/paneling_00123.png", "Palette_droite_Principale/Boutons/Construire des maison/Maisons_Click.png")

        self.button_131 = Button_img(
            self.width-80, 294+21, "ingamehud/paneling_00131.png")
        self.button_135 = Button_img(
            self.width-30, 294+21,  "ingamehud/paneling_00135.png")
        #
        self.button_127 = Button_img(
            self.width-130, 330+21,  "ingamehud/paneling_00127.png")
        self.button_163 = Button_img(
            self.width-80, 330+21,  "ingamehud/paneling_00163.png")
        self.button_151 = Button_img(
            self.width-30, 330+21,  "ingamehud/paneling_00151.png")
        #

        self.button_147 = Button_img(
            self.width-130, 366+21,  "ingamehud/paneling_00147.png")
        self.button_143 = Button_img(
            self.width-80, 366+21,  "ingamehud/paneling_00143.png")
        self.button_139 = Button_img(
            self.width-30, 366+21,  "ingamehud/paneling_00139.png")
        #
        self.button_167 = Button_img(
            self.width-130, 402+21,  "ingamehud/paneling_00167.png")
        self.button_159 = Button_img(
            self.width-80, 402+21,  "ingamehud/paneling_00159.png")
        self.button_155 = Button_img(
            self.width-30, 402+21,  "ingamehud/paneling_00155.png")
        #
        self.button_246 = Button_img(
            self.width-130, 438+21,  "ingamehud/paneling_00246.png")
        self.button_115 = Button_img(
            self.width-80, 436+21,  "ingamehud/paneling_00115.png")
        self.button_122 = Button_img(
            self.width-30, 436+21,  "ingamehud/paneling_00122.png")
        #
        self.mini_button = {"098": self.button_098, "080": self.button_080, "082": self.button_082, "085":
                            self.button_085, "088": self.button_088, "091": self.button_091, "094": self.button_094, }
        #
        self.main_button = {"house": self.button_123, "shovel": self.button_131, "road": self.button_135, "water": self.button_127, "medic": self.button_163, "thunder": self.button_151,
                            "scroll": self.button_147, "mask": self.button_143, "bighouse": self.button_139, "hammer": self.button_167, "sword": self.button_159, "wagon": self.button_155,
                            "X": self.button_246, "notice": self.button_115, "bell": self.button_122}

        self.cursor = {"house": pg.cursors.Cursor((30, 30), pg.image.load(
            "cursor/hammer.png").convert_alpha())}

    def draw(self, screen):
        screen.blit(self.paneling_017, (self.width - 162, 4+21))
        screen.blit(self.map_panels_00003, (self.width - 162, 450+4+21))
        screen.blit(self.map_panels_00003, (self.width - 162, 1000))
        screen.blit(self.panelwindow_013, (self.width-162+6, 216+4+21))

        for mini in self.mini_button.values():
            mini.show(screen)
        for main in self.main_button.values():
            main.show(screen)

    def update(self, mouse_pos, mouse_action):
        for main in self.main_button.items():
            if main[1].IsHoverOn(mouse_pos):
                if main[1].Clicked(mouse_action):
                    pg.mouse.set_cursor(self.cursor[main[0]])
                    self.interaction = main[0]

        if mouse_action[2] or self.interaction == None:
            pg.mouse.set_cursor(
                pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
            self.interaction = None
