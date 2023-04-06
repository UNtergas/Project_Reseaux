# Fichier pour nos constantes
import pygame
pygame.init()

# font scene Pre_Menu
font0 = pygame.font.SysFont('JSL ANCIENT', 24, True)
# font scene Menu
font1 = pygame.font.SysFont('JSL ANCIENT', 48, True)

# foot scene New_game
font2 = pygame.font.SysFont('JSL ANCIENT', 46, True)

# foot scene Load_game
font_button = pygame.font.SysFont('JSL ANCIENT', 48, True)

font_save = pygame.font.SysFont('JSL ANCIENT', 48, True)

screen_height = 1024
screen_width = 768

MAP_SIZE = (40, 40)
TILE_SIZE = 40
event_types = {"LaunchGame": 100, "LoadName": 200}

FIRE_THRESHOLD = 20
COLLAPSE_THESHOLD = 20
BURNING_TIME = 20

scaleDelta = TILE_SIZE/60

LAND1A_078 = pygame.image.load("newland/Land1a_00078.png")
LAND1A_035 = pygame.image.load("newland/Land1a_00035.png")
LAND1A_036 = pygame.image.load("newland/Land1a_00036.png")
LAND1A_049 = pygame.image.load("newland/Land1a_00049.png")
LAND1A_057 = pygame.image.load("newland/Land1a_00057.png")
LAND1A_058 = pygame.image.load("newland/Land1a_00058.png")
LAND1A_060 = pygame.image.load("newland/Land1a_00060.png")
LAND1A_061 = pygame.image.load("newland/Land1a_00061.png")
LAND1A_120 = pygame.image.load("newland/Land1a_00120.png")
LAND1A_128 = pygame.image.load("newland/Land1a_00128.png")
LAND1A_133 = pygame.image.load("newland/Land1a_00133.png")
LAND1A_139 = pygame.image.load("newland/Land1a_00139.png")
LAND1A_143 = pygame.image.load("newland/Land1a_00143.png")
LAND1A_147 = pygame.image.load("newland/Land1a_00147.png")
LAND1A_148 = pygame.image.load("newland/Land1a_00148.png")
LAND1A_152 = pygame.image.load("newland/Land1a_00152.png")
LAND1A_159 = pygame.image.load("newland/Land1a_00159.png")
LAND1A_170 = pygame.image.load("newland/Land1a_00170.png")
LAND1A_171 = pygame.image.load("newland/Land1a_00171.png")
LAND1A_172 = pygame.image.load("newland/Land1a_00172.png")
LAND1A_173 = pygame.image.load("newland/Land1a_00120.png")
LAND1A_234 = pygame.image.load("newland/Land1a_00234.png")
LAND1A_235 = pygame.image.load("newland/Land1a_00235.png")
LAND2A_095 = pygame.image.load("newland/Land2a_00095.png")
LAND3A_071 = pygame.image.load("newland/land3a_00071.png")
LAND3A_072 = pygame.image.load("newland/land3a_00072.png")
LAND3A_074 = pygame.image.load("newland/land3a_00074.png")
LAND3A_081 = pygame.image.load("newland/land3a_00081.png")
LAND3A_082 = pygame.image.load("newland/land3a_00082.png")


GRASS_IMAGE = pygame.image.load("newland/Land1a_00285.png")

#
TEMP_BUILD = pygame.image.load("fonction_render/house/Land2a_00001.png")
# fonction
HOUSE_01 = pygame.image.load(
    "fonction_render/house/Housng1a_00045.png")
ROAD = pygame.image.load(
    "fonction_render/road/Land2a_00044.png")
PERFECTURE = pygame.image.load(
    "fonction_render/house/Security_00001.png")
ENGINEER = pygame.image.load(
    "fonction_render/house/transport_00056.png")
WELL = pygame.image.load(
    "fonction_render/house/Utilitya_00001.png")

HOUSE_01 = pygame.transform.rotozoom(HOUSE_01, 0, scaleDelta)
ROAD = pygame.transform.rotozoom(ROAD, 0, scaleDelta)
PERFECTURE = pygame.transform.rotozoom(PERFECTURE, 0, scaleDelta)
GRASS_IMAGE = pygame.transform.rotozoom(GRASS_IMAGE, 0, scaleDelta)
WELL = pygame.transform.rotozoom(WELL, 0, scaleDelta)
ENGINEER = pygame.transform.rotozoom(ENGINEER, 0, scaleDelta)
TEMP_BUILD = pygame.transform.rotozoom(TEMP_BUILD, 0, scaleDelta)


TEMP_TILE = {
    "house": HOUSE_01, "shovel": GRASS_IMAGE, "road": ROAD, "sword": PERFECTURE,
    "hammer": ENGINEER, "water": WELL, "blank": TEMP_BUILD
}

RUMBLE_OF_BUILDING = pygame.transform.rotozoom(pygame.image.load(
    "fonction_render/burning/useless_tile.png"), 0, scaleDelta)

# modulo 8
JUST_A_BURNING_MEMORY = {0: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_1.png"), 0, scaleDelta),
                         1: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_2.png"), 0, scaleDelta),
                         2: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_3.png"), 0, scaleDelta),
                         3: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_4.png"), 0, scaleDelta),
                         4: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_5.png"), 0, scaleDelta),
                         5: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_6.png"), 0, scaleDelta),
                         6: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_7.png"), 0, scaleDelta),
                         7: pygame.transform.rotozoom(pygame.image.load("fonction_render/burning/burn_8.png"), 0, scaleDelta)
                         }


OVERLAY_COMPONENT = {"white_top": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/white_top.png"), 0, scaleDelta),
                     "white_bot": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/white_bot.png"), 0, scaleDelta),
                     "yellow_top": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/yellow_top.png"), 0, scaleDelta),
                     "yellow_mid": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/yellow_mid.png"), 0, scaleDelta),
                     "yellow_bot": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/yellow_bot.png"), 0, scaleDelta),
                     "orange_top":  pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/orange_top.png"), 0, scaleDelta),
                     "orange_mid": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/orange_mid.png"), 0, scaleDelta),
                     "orange_bot":  pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/orange_bot.png"), 0, scaleDelta),
                     "red_top": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/red_top.png"), 0, scaleDelta),
                     "red_mid": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/red_mid.png"), 0, scaleDelta),
                     "red_bot": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/red_bot.png"), 0, scaleDelta)
                     }
top_w, top_h = OVERLAY_COMPONENT["white_top"].get_size()  # 96x66
bot_w, bot_h = OVERLAY_COMPONENT["white_bot"].get_size()  # 80x68
mid_w, mid_h = OVERLAY_COMPONENT["yellow_mid"].get_size()  # 48x20

# 15-30  piller
stat_15_30 = pygame.Surface((top_w, top_h+bot_h-mid_h), pygame.SRCALPHA)
stat_15_30.blit(OVERLAY_COMPONENT["white_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h))
stat_15_30.blit(OVERLAY_COMPONENT["white_top"], (0, 0))

# 30-45 piller
stat_30_45 = pygame.Surface((top_w, top_h+bot_h-mid_h), pygame.SRCALPHA)
stat_30_45.blit(OVERLAY_COMPONENT["yellow_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h))
stat_30_45.blit(OVERLAY_COMPONENT["yellow_top"], (0, 0))

# 45-60 piller
stat_45_60 = pygame.Surface(
    (top_w, top_h+bot_h-mid_h+2*mid_h), pygame.SRCALPHA)
stat_45_60.blit(OVERLAY_COMPONENT["yellow_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h+2*mid_h))
# mid_length
stat_45_60.blit(OVERLAY_COMPONENT["yellow_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+mid_h)))
stat_45_60.blit(OVERLAY_COMPONENT["yellow_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+2*mid_h)))
#
stat_45_60.blit(OVERLAY_COMPONENT["yellow_top"], (0, 0))

# 60-75 piller
stat_60_75 = pygame.Surface(
    (top_w, top_h+bot_h-mid_h+2*mid_h), pygame.SRCALPHA)
stat_60_75.blit(OVERLAY_COMPONENT["orange_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h+2*mid_h))
# mid_length
stat_60_75.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+mid_h)))
stat_60_75.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+2*mid_h)))
#
stat_60_75.blit(OVERLAY_COMPONENT["orange_top"], (0, 0))

# 75-90 piller
stat_75_90 = pygame.Surface(
    (top_w, top_h+bot_h-mid_h+4*mid_h), pygame.SRCALPHA)
stat_75_90.blit(OVERLAY_COMPONENT["orange_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h+4*mid_h))
# mid_length
stat_75_90.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+mid_h)))
stat_75_90.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+2*mid_h)))
stat_75_90.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+3*mid_h)))
stat_75_90.blit(OVERLAY_COMPONENT["orange_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+4*mid_h)))
#
stat_75_90.blit(OVERLAY_COMPONENT["orange_top"], (0, 0))

# 90> piller
stat_90 = pygame.Surface(
    (top_w, top_h+bot_h-mid_h+6*mid_h), pygame.SRCALPHA)
stat_90.blit(OVERLAY_COMPONENT["red_bot"], (stat_15_30.get_width(
)-bot_w-top_w/2+bot_w/2, stat_15_30.get_height()-bot_h+6*mid_h))
# mid_length
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+mid_h)))
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+2*mid_h)))
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+3*mid_h)))
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+4*mid_h)))
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+5*mid_h)))
stat_90.blit(OVERLAY_COMPONENT["red_mid"], ((stat_15_30.get_width(
)-mid_w-top_w/2+mid_w/2, stat_15_30.get_height()-bot_h+6*mid_h)))
#
stat_90.blit(OVERLAY_COMPONENT["red_top"], (0, 0))

OVERLAY = {"fond": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/fond.png"), 0, scaleDelta),
           "big_fond": pygame.transform.rotozoom(pygame.image.load("fonction_render/Overlay/big_fond.png"), 0, scaleDelta),
           "15<": OVERLAY_COMPONENT["white_bot"],
           "15-30": stat_15_30,
           "30-45": stat_30_45,
           "45-60": stat_45_60,
           "60-75": stat_60_75,
           "75-90": stat_75_90,
           ">90": stat_90
           }

OVERLAY_WATER = {"nowater": pygame.transform.rotozoom(pygame.image.load("fonction_render/house/Land2a_00001.png"), 0, scaleDelta),
                 "yeswater": pygame.transform.rotozoom(pygame.image.load("fonction_render/house/Land2a_00017.png"), 0, scaleDelta)}

thickarrow_strings = (  # sized 24x24
    "XX                      ",
    "XXX                     ",
    "XXXX                    ",
    "XX.XX                   ",
    "XX..XX                  ",
    "XX...XX                 ",
    "XX....XX                ",
    "XX.....XX               ",
    "XX......XX              ",
    "XX.......XX             ",
    "XX........XX            ",
    "XX........XXX           ",
    "XX......XXXXX           ",
    "XX.XXX..XX              ",
    "XXXX XX..XX             ",
    "XX   XX..XX             ",
    "     XX..XX             ",
    "      XX..XX            ",
    "      XX..XX            ",
    "       XXXX             ",
    "       XX               ",
    "                        ",
    "                        ",
    "                        ")
rail_strings = (  # sized 24x24
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "X....................X  ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "X....................X  ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "X....................X  ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "  X.X            X.X    ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "X....................X  ",
    "XXX.XXXXXXXXXXXXXX.XXX  ",
    "  X.X            X.X    ")
shovel_strings = (  # 32x32
    "XX                         XX   ",
    "XXX                       XXXX  ",
    "XXXX                     XX.XXX ",
    "XX.XX                    X...XXX",
    "XX..XX                   XX...XX",
    "XX...XX                 XXXX.XX ",
    "XX....XX               XX.XXXX  ",
    "XX.....XX             XX.XX     ",
    "XX.....XXX           XX.XX      ",
    "XX...XXXXXX         XX.XX       ",
    "XX..XX             XX.XX        ",
    "XX.X              XX.XX         ",
    "XX               XX.XX          ",
    "X               XX.XX           ",
    "               XX.XX            ",
    "              XX.XX             ",
    "             XX.XX              ",
    "       X    XX.XX               ",
    "      XXXX XX.XX                ",
    "     X..XXXX.XX                 ",
    "    X....XX.XX                  ",
    "   X....XX.XX                   ",
    "  X....X.XXXXX                  ",
    " X....X...X.XX                  ",
    " X...X...X...XX                 ",
    "X.......X....X                  ",
    "X......X....X                   ",
    "X..........X                    ",
    "X.........X                     ",
    "X........X                      ",
    " X.....XX                       ",
    "  XXXXX                         "
)

hammer_strings = (  # 32x32
    "XX                              ",
    "XXX                             ",
    "XXXX                            ",
    "XX.XX                           ",
    "XX..XX                          ",
    "XX...XX                         ",
    "XX....XX                        ",
    "XX.....XX                       ",
    "XX.....XXX                      ",
    "XX...XXXXXX                     ",
    "XX..XX                          ",
    "XX.X                            ",
    "XX            X......X          ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "      XXXXXXXXXXXXXXXXXXXXXX    ",
    "             XXX..XXX           ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "               X..X             ",
    "              XXXXXX            "
)

arrow_strings = (  # 32x32
    " X                              ",
    " X.X                            ",
    " X.XX                           ",
    " X..XX                          ",
    " X...XX                         ",
    " X....XX                        ",
    " X.....XX                       ",
    " X......XX                      ",
    " X.......XX                     ",
    " X........XX                    ",
    " X.........XX                   ",
    " X..........XX                  ",
    " X...........XX                 ",
    " X............XX                ",
    " X.............XX               ",
    " X..............XX              ",
    " X...............XX             ",
    " X................XX            ",
    " X......XXXXXXXXXXXXX           ",
    " X.....XXXX                     ",
    " X....XX                        ",
    " X...X                          ",
    " X..X                           ",
    " X.X                            ",
    " XX                             ",
    " X                              ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                "
)
