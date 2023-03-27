
import pygame as pg
# import random
from .setting import *


class World:

    def __init__(self, grid_l_x, grid_l_y, width, height, mattrice, hud):
        self.grid_lx = grid_l_x
        self.grid_ly = grid_l_y
        self.width = width
        self.height = height
        self.hud = hud
        self.mattrice = mattrice

        self.land_tile = pg.Surface(
            (self.grid_lx * TILE_SIZE, self.grid_ly * TILE_SIZE))
        # self.land_tile = pg.Surface((self.width, self.height)).co2nvert_alpha()
        self.tiles = self.load_images()
        self.tiles_event = self.load_image_event()
        self.world = self.cree_world(self.mattrice)
        self.boundary = [self.land_tile.get_height, self.land_tile.get_width]
        self.temp_tile = None
        #
        #

    def update(self, mouse_pos, mouse_action, camera):
        self.temp_tile = None
        if self.hud["main"].interaction != None:
            grid_pos = self.mouse_to_grid(
                mouse_pos[0], mouse_pos[1], camera.scroll)

            print(f"grid{grid_pos}")
            if self.can_place_tile(grid_pos, mouse_pos):
                img = self.tiles_event[self.hud["main"].interaction]
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                print(f"pos{iso_poly},collision{collision}")
                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }
                if mouse_action[0] and not collision:
                    self.world[grid_pos[0]][grid_pos[1]
                                            ]["tile"] = DEFAULT_HOUSING[self.hud["main"].interaction]
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud["main"].interaction = None

    def cree_world(self, mattrice):
        world = []

        for grid_x in range(self.grid_lx):
            world.append([])
            for grid_y in range(self.grid_ly):
                world_tile = self.grid_to_world(grid_x, grid_y, mattrice)
                world[grid_x].append(world_tile)

            #
            #           render image alongside with grid init
            #
                render_pos = world_tile["render_pos"]
                self.land_tile.blit(
                    self.tiles["land"], (render_pos[0] + self.land_tile.get_width()*0.5, render_pos[1]))
        return world
        #
        #          WORLD=[  [output(0,0),output(0,1)....,output(0,gridy)],
        #                .....
        #                   [output(gridx,0),.....,output(gridx,gridy)]      ]
        #

    def draw(self, camera, screen):

        screen.fill((0, 0, 0))
        screen.blit(self.land_tile,
                    (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_lx):
            for y in range(self.grid_ly):
                render_pos = self.world[x][y]["render_pos"]

#                   different tiles
#
                if self.world[x][y]["tile"]["name"] != "":
                    name_tile = self.world[x][y]["tile"]["name"]
                    offset = self.world[x][y]["tile"]["offset"]
                    screen.blit(self.tiles[name_tile], (
                        render_pos[0]+self.land_tile.get_width() *
                        0.5 + camera.scroll.x,
                        render_pos[1]+self.land_tile.get_height()*0 - offset + camera.scroll.y))
#
#                   2.5D grid
                p = self.world[x][y]["iso_poly"]
                p = [(x + self.land_tile.get_width() *
                      0.5 + camera.scroll.x, y + self.land_tile.get_height()*0+camera.scroll.y) for x, y in p]
                pg.draw.polygon(screen, (0, 0, 0), p, 1)
        if self.temp_tile != None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.land_tile.get_width()/2 +
                         camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.land_tile.get_width() /
                    2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() -
                                     TILE_SIZE) + camera.scroll.y
                )
            )

    def grid_to_world(self, grid_x, grid_y, mattrix):

        rect = [
            (grid_x*TILE_SIZE, grid_y*TILE_SIZE),
            (grid_x*TILE_SIZE+TILE_SIZE, grid_y*TILE_SIZE),
            (grid_x*TILE_SIZE+TILE_SIZE, grid_y*TILE_SIZE+TILE_SIZE),
            (grid_x*TILE_SIZE, grid_y*TILE_SIZE+TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        # find minimum pos for x,y because pygame.surface.blit take arg of
        # the upper left corner of the blit or a Rect when start drawing
        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        output = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": matchcasetileval(mattrix, grid_x, grid_y),
            "collision": True if matchcasetileval(mattrix, grid_x, grid_y)["name"] != "" else False
        }

        return output

    def mouse_to_grid(self, x, y, scroll):
        # remove camera scrolling & offset
        world_x = x - scroll.x - self.land_tile.get_height()*0.5
        world_y = y - scroll.y
        # transform iso to cartesian
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform back to grid matrix
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def can_place_tile(self, grid_pos, mouse_pos):
        mouse_on_panel = False
        for rect in [self.hud["up"].rect, self.hud["main"].rect, self.hud["fps"].rect, self.hud["pop"].rect]:
            if rect.collidepoint(mouse_pos):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_lx) and (
            0 <= grid_pos[1] <= self.grid_ly)
        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

    def load_images(self):

        land = LAND1A_078.convert_alpha()
        l1a35 = LAND1A_035.convert_alpha()
        l1a36 = LAND1A_036.convert_alpha()
        l1a49 = LAND1A_049.convert_alpha()
        l1a57 = LAND1A_057.convert_alpha()
        l1a58 = LAND1A_058.convert_alpha()
        l1a60 = LAND1A_060.convert_alpha()
        l1a61 = LAND1A_061.convert_alpha()
        l1a120 = LAND1A_120.convert_alpha()
        l1a128 = LAND1A_128.convert_alpha()
        l1a133 = LAND1A_133.convert_alpha()
        l1a139 = LAND1A_139.convert_alpha()
        l1a143 = LAND1A_143.convert_alpha()
        l1a147 = LAND1A_147.convert_alpha()
        l1a148 = LAND1A_148.convert_alpha()
        l1a152 = LAND1A_152.convert_alpha()
        l1a159 = LAND1A_159.convert_alpha()
        l1a170 = LAND1A_170.convert_alpha()
        l1a171 = LAND1A_171.convert_alpha()
        l1a172 = LAND1A_172.convert_alpha()
        l1a173 = LAND1A_173.convert_alpha()
        l1a234 = LAND1A_234.convert_alpha()
        l1a235 = LAND1A_235.convert_alpha()
        l1a285 = LAND1A_285.convert_alpha()
        l2a095 = LAND2A_095.convert_alpha()
        l3a071 = LAND3A_071.convert_alpha()
        l3a072 = LAND3A_072.convert_alpha()
        l3a074 = LAND3A_074.convert_alpha()
        l3a081 = LAND3A_081.convert_alpha()
        l3a082 = LAND3A_082.convert_alpha()

        house1 = HOUSE_01.convert_alpha()
        return {"land": land,
                "l1a35": l1a35, "l1a36": l1a36, "l1a49": l1a49, "l1a57": l1a57, "l1a58": l1a58, "l1a60": l1a60, "l1a61": l1a61,
                "l1a120": l1a120, "l1a128": l1a128, "l1a133": l1a133, "l1a139": l1a139, "l1a143": l1a143, "l1a147": l1a147, "l1a148": l1a148,
                "l1a152": l1a152, "l1a159": l1a159, "l1a170": l1a170, "l1a171": l1a171, "l1a172": l1a172, "l1a173": l1a173, "l1a234": l1a234,
                "l1a235": l1a235, "12a285": l1a285,
                "l2a095": l2a095,
                "l3a071": l3a071, "l3a072": l3a072, "l3a074": l3a074, "l3a081": l3a081, "l3a082": l3a082,
                "house": house1}

    def load_image_event(self):
        house1 = HOUSE_01.convert_alpha()

        return {"house": house1
                }
