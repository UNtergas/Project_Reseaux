import pygame as pg
from Button import *
from const import shovel_strings, rail_strings, hammer_strings, arrow_strings


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


class Time_Wizard:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.image = pg.image.load(
            "ingamehud/paneling_00510.png").convert_alpha()
        self.rect = pg.Rect(x, y, width, height)
        self.speed_show = InfoShow(
            self.x+20, self.y+20, "Speed=100%", 20, (255, 255, 255))
        self.increase = Button_img(
            self.x+30, self.y+80, None, "Palette_droite_Principale/Boutons/Time_Wizard/system_00015.png", "Palette_droite_Principale/Boutons/Time_Wizard/system_00016.png")
        # gap 77/ 2 long af button
        self.decrease = Button_img(
            self.x+60, self.y+80, None, "Palette_droite_Principale/Boutons/Time_Wizard/system_00017.png", "Palette_droite_Principale/Boutons/Time_Wizard/system_00018.png")
        self.pause_button = Button_img(
            self.x+120, self.y+80, None, "ingamehud/paneling_00098.png")
        self.ispause = False
        self.history = 0

    def update(self, time, mouse_pos, mouse_action):
        # print(f"speed:{time}")
        if self.decrease.IsHoverOn(mouse_pos):
            if mouse_action[0]:
                if self.ispause:
                    time = self.history
                    self.ispause = False

                if time <= 0.25:
                    time = 0.25
                else:
                    time -= 0.25
        elif self.increase.IsHoverOn(mouse_pos):
            if mouse_action[0]:
                if self.ispause:
                    time = self.history
                    self.ispause = False
                if time >= 2:
                    time = 2.0
                else:
                    time += 0.25
        elif self.pause_button.IsHoverOn(mouse_pos):
            if mouse_action[0]:
                if self.ispause:
                    time = self.history
                    self.ispause = False
                else:
                    self.history = time
                    time = 0
                    self.ispause = True
        if time == 0:
            self.speed_show.text = "Pause"
        else:
            self.speed_show.text = 'Speed={}%'.format(time*100)
        return time

    def draw(self, screen):
        screen.blit(pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height)), self.rect)
        self.speed_show.draw(screen)
        self.decrease.show(screen)
        self.increase.show(screen)
        self.pause_button.show(screen)


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
        self.overlay = InfoShow(
            self.width-160, 30, "normal", 20, (255, 255, 255))
        self.paneling_017 = pg.image.load(
            "ingamehud/paneling_00017.png").convert_alpha()

        self.rect = pg.Rect((self.width - 162, 25),
                            (self.paneling_017.get_width(), self.height-25))

        self.map_panels_00003 = pg.image.load(
            "ingamehud/map_panels_00003.png").convert_alpha()
        self.panelwindow_list = {None: pg.image.load(
            "ingamehud/panelwindows_00013.png").convert_alpha(), "house": pg.image.load("ingamehud/window_interactive/house.png").convert_alpha(), "shovel": pg.image.load("ingamehud/window_interactive/shovel.png").convert_alpha(),
            "road": pg.image.load("ingamehud/window_interactive/road.png").convert_alpha(), "water": pg.image.load("ingamehud/window_interactive/water.png").convert_alpha(), "medic": pg.image.load("ingamehud/window_interactive/medic.png").convert_alpha(),
            "thunder": pg.image.load("ingamehud/window_interactive/thunder.png").convert_alpha(), "scroll": pg.image.load("ingamehud/window_interactive/scroll.png").convert_alpha(), "mask": pg.image.load("ingamehud/window_interactive/mask.png").convert_alpha(),
            "bighouse": pg.image.load("ingamehud/window_interactive/bighouse.png").convert_alpha(), "hammer": pg.image.load("ingamehud/window_interactive/hammer.png").convert_alpha(), "sword": pg.image.load("ingamehud/window_interactive/sword.png").convert_alpha(),
            "wagon": pg.image.load("ingamehud/window_interactive/wagon.png").convert_alpha(), "X": pg.image.load("ingamehud/panelwindows_00013.png").convert_alpha(), "notice": pg.image.load("ingamehud/panelwindows_00013.png").convert_alpha(), "bell": pg.image.load("ingamehud/panelwindows_00013.png").convert_alpha()
        }
        #hud in out
        self.button_098 = Button_img(
            self.width-20, 20+21, None, "ingamehud/paneling_00098.png",)
        # gap 77/ 2 long af button
        self.button_080 = Button_img(
            self.width-120, 170+21, None, "ingamehud/paneling_00080.png")
        self.button_082 = Button_img(
            self.width-43, 170+21, None,  "ingamehud/paneling_00082.png")
        # gap 39 /small button
        self.button_085 = Button_img(
            self.width-139, 199+21, None,  "ingamehud/paneling_00085.png")
        self.button_088 = Button_img(
            self.width-100, 199+21, None,  "ingamehud/paneling_00088.png")
        self.button_091 = Button_img(
            self.width-62, 199+21, None,  "ingamehud/paneling_00091.png")
        self.button_094 = Button_img(
            self.width-23, 199+21, None,  "ingamehud/paneling_00094.png")
        # gap width 50 gap height 36 /big button
        self.button_123 = Button_img(
            self.width-130, 294+21, None,  "ingamehud/paneling_00123.png", "Palette_droite_Principale/Boutons/CLICK/Maisons_Click.png")

        self.button_131 = Button_img(
            self.width-80, 294+21, None, "ingamehud/paneling_00131.png", "Palette_droite_Principale/Boutons/CLICK/Clear_Land_Click.png")
        self.button_135 = Button_img(
            self.width-30, 294+21, None,  "ingamehud/paneling_00135.png", "Palette_droite_Principale/Boutons/CLICK/Route_Click.png")
        #
        self.button_127 = Button_img(
            self.width-130, 330+21, None,  "ingamehud/paneling_00127.png", "Palette_droite_Principale/Boutons/CLICK/Water_Click.png")
        self.button_163 = Button_img(
            self.width-80, 330+21, None,  "ingamehud/paneling_00163.png", "Palette_droite_Principale/Boutons/CLICK/Health_Click.png")
        self.button_151 = Button_img(
            self.width-30, 330+21, None,  "ingamehud/paneling_00151.png", "Palette_droite_Principale/Boutons/CLICK/religion_Click.png")
        #

        self.button_147 = Button_img(
            self.width-130, 366+21, None,  "ingamehud/paneling_00147.png", "Palette_droite_Principale/Boutons/CLICK/Education_Click.png")
        self.button_143 = Button_img(
            self.width-80, 366+21, None,  "ingamehud/paneling_00143.png", "Palette_droite_Principale/Boutons/CLICK/Divertisment_Click.png")
        self.button_139 = Button_img(
            self.width-30, 366+21, None,  "ingamehud/paneling_00139.png", "Palette_droite_Principale/Boutons/CLICK/Admin_Gouv_Click.png")
        #
        self.button_167 = Button_img(
            self.width-130, 402+21, None,  "ingamehud/paneling_00167.png", "Palette_droite_Principale/Boutons/CLICK/ingineer_Click.png")
        self.button_159 = Button_img(
            self.width-80, 402+21, None,  "ingamehud/paneling_00159.png", "Palette_droite_Principale/Boutons/CLICK/Security_struct_Click.png")
        self.button_155 = Button_img(
            self.width-30, 402+21, None,  "ingamehud/paneling_00155.png", "Palette_droite_Principale/Boutons/CLICK/Trade_Click.png")
        #
        self.button_246 = Button_img(
            self.width-130, 438+21, None,  "ingamehud/paneling_00246.png")
        self.button_115 = Button_img(
            self.width-80, 436+21, None,  "ingamehud/paneling_00115.png", "Palette_droite_Principale/Boutons/CLICK/PopUp_Click.png")
        self.button_122 = Button_img(
            self.width-30, 436+21, None,  "ingamehud/paneling_00122.png")
        #
        self.mini_button = {"098": self.button_098, "080": self.button_080, "082": self.button_082, "085":
                            self.button_085, "088": self.button_088, "091": self.button_091, "094": self.button_094, }
        #
        self.main_button = {"house": self.button_123, "shovel": self.button_131, "road": self.button_135, "water": self.button_127, "medic": self.button_163, "thunder": self.button_151,
                            "scroll": self.button_147, "mask": self.button_143, "bighouse": self.button_139, "hammer": self.button_167, "sword": self.button_159, "wagon": self.button_155,
                            "X": self.button_246, "notice": self.button_115, "bell": self.button_122}

        self.cursor_default = pg.cursors.Cursor(
            (32, 32), (0, 0), *pg.cursors.compile(arrow_strings))
        hammer_cursor = pg.cursors.Cursor(
            (32, 32), (0, 0), *pg.cursors.compile(hammer_strings))
        shovel_cursor = pg.cursors.Cursor(
            (32, 32), (0, 0), *pg.cursors.compile(shovel_strings))
        road_cursor = pg.cursors.Cursor(
            (24, 24), (0, 0), *pg.cursors.compile(rail_strings))
        self.cursor = {"house": hammer_cursor, "shovel": shovel_cursor, "road": road_cursor, "water": hammer_cursor, "medic": self.cursor_default, "thunder": self.cursor_default,
                       "scroll": self.cursor_default, "mask": self.cursor_default, "bighouse": self.cursor_default, "hammer": hammer_cursor, "sword": hammer_cursor,
                       "wagon": self.cursor_default, "X": self.cursor_default, "notice": self.cursor_default, "bell": self.cursor_default}

    def draw(self, screen):
        # self.overlay.draw(screen)
        screen.blit(self.paneling_017, (self.width - 162, 4+21))
        screen.blit(self.map_panels_00003, (self.width - 162, 575))
        # screen.blit(self.map_panels_00003, (self.width - 162, 1000))
        screen.blit(
            self.panelwindow_list[self.interaction], (self.width-162+6, 216+4+21))

        for mini in self.mini_button.values():
            mini.show(screen)
        for main in self.main_button.values():
            main.show(screen)
        self.overlay.draw(screen)

    def update(self, mouse_pos, mouse_action):
        for main in self.main_button.items():
            if main[1].IsHoverOn(mouse_pos):
                if main[1].Clicked(mouse_action):
                    # pg.mouse.set_cursor(self.cursor[main[0]])
                    self.interaction = main[0]

        if mouse_action[2] or self.interaction == None:
            # pg.mouse.set_cursor(
            #     # self.cursor_default)
            self.interaction = None
