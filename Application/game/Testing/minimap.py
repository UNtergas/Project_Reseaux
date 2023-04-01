import pygame as pg
from game.setting import DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT, NUMS_GRID_Y, NUMS_GRID_X, TILE_SIZE
from events.event_manager import EventManager
from .mapcontroller import MapController
from map_element.tile import Tile
from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from .utils import scale_image
from .textures import Textures


class MiniMap:

    scale_down_ratio = 0.0249

    def __init__(self, width, height, logic_grid) -> None:

        self.screen_width = width
        self.screen_height = height

        self.mini_screen_width = MiniMap.scale_down_ratio * width
        self.mini_screen_height = MiniMap.scale_down_ratio * height

        self.mini_default_surface_width = MiniMap.scale_down_ratio * DEFAULT_SURFACE_WIDTH
        self.mini_default_surface_height = MiniMap.scale_down_ratio * DEFAULT_SURFACE_HEIGHT

        self.mini_default_surface = pg.Surface(
            (self.mini_default_surface_width, self.mini_default_surface_height))

        self.mini_screen_rect = None

        # self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width
        # self.mini_map_pos_y = self.screen_height * 0.04
        self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width - 8
        self.mini_map_pos_y = 98

        self.mini_relative_x = None
        self.mini_relative_y = None

        self.mini_default_surface_generator(logic_grid)

        EventManager.register_mouse_listener(self.mini_map_mouse_listener)

    def mini_map_mouse_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        (x, y) = mouse_pos
        if (self.mini_map_pos_x <= x <= self.screen_width) and (self.mini_map_pos_y < y <= self.mini_map_pos_y + self.mini_default_surface_height):
            if mouse_action[0]:
                self.mini_relative_x = x - self.mini_map_pos_x
                self.mini_relative_y = y - self.mini_map_pos_y
            else:
                self.mini_relative_x = None
                self.mini_relative_y = None

    def mini_default_surface_generator(self, logic_grid):
        for row in range(NUMS_GRID_Y):
            for col in range(NUMS_GRID_X):
                tile: Tile = logic_grid[row][col]
                (x, y) = tile.get_render_coord()
                # cell is placed at 1/2 default_surface.get_width() and be offseted by the position of the default_surface
                (x_offset, y_offset) = (x + DEFAULT_SURFACE_WIDTH / 2, y)
                (mini_x_offset, mini_y_offset) = (x_offset *
                                                  MiniMap.scale_down_ratio, y_offset*MiniMap.scale_down_ratio)
                texture_image = Textures.get_texture(TileTypes.GRASS)
                mini_texture_image = scale_image(texture_image, texture_image.get_width(
                )*MiniMap.scale_down_ratio, texture_image.get_height()*MiniMap.scale_down_ratio)

                self.mini_default_surface.blit(mini_texture_image,
                                               (mini_x_offset, mini_y_offset - texture_image.get_height() + TILE_SIZE))

    def update_mini_default_surface(self, logic_grid):
        for row in range(NUMS_GRID_Y):
            for col in range(NUMS_GRID_X):
                tile: Tile = logic_grid[row][col]
                (x, y) = tile.get_render_coord()
                # cell is placed at 1/2 default_surface.get_width() and be offseted by the position of the default_surface
                (x_offset, y_offset) = (x + DEFAULT_SURFACE_WIDTH / 2, y)

                (mini_x_offset, mini_y_offset) = (x_offset *
                                                  MiniMap.scale_down_ratio, y_offset*MiniMap.scale_down_ratio)

                (relative_x, relative_y) = (mini_x_offset +
                                            self.mini_map_pos_x, mini_y_offset + self.mini_map_pos_y)
                color = self.get_color(tile)
                self.mini_default_surface.fill(
                    color, ((mini_x_offset, mini_y_offset), (1, 1)))

    def update(self, map_controller: MapController, logic_grid):
        if self.mini_relative_x is not None and self.mini_relative_y is not None:
            corresponding_x = - \
                (self.mini_relative_x - self.mini_screen_width/2) / \
                self.scale_down_ratio
            corresponding_y = - \
                (self.mini_relative_y - self.mini_screen_height/2) / \
                self.scale_down_ratio
            map_controller.set_map_pos(corresponding_x, corresponding_y)

        self.update_mini_default_surface(logic_grid)

    def draw(self, screen, map_pos, logic_grid: [[Tile]]):
        self.mini_screen_rect = pg.Rect(- map_pos[0] * MiniMap.scale_down_ratio + self.mini_map_pos_x,
                                        - map_pos[1] * MiniMap.scale_down_ratio + self.mini_map_pos_y,
                                        self.mini_screen_width, self.mini_screen_height)
        screen.blit(self.mini_default_surface,
                    (self.mini_map_pos_x, self.mini_map_pos_y))
        pg.draw.rect(screen, (255, 255, 0), self.mini_screen_rect, 1)

    def get_color(self, tile: Tile):
        color = (0, 255, 0)
        if tile.get_building() is not None:
            return (255, 255, 0)  # yellow

        if tile.get_road() is not None:
            # brown
            return (153, 76, 0)

        match tile.type:
            case TileTypes.WATER: return (102, 178, 255)  # blue

            case TileTypes.WHEAT: return (204, 204, 0)  # Bold yellow

            case TileTypes.ROCK: return (96, 96, 96)  # Gray

            case TileTypes.GRASS: return (76, 153, 0)

            case TileTypes.TREE: return (204, 255, 204)
